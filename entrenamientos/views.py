from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
import json
from .forms import *
from .models import (
    Atleta,
    Atletas_Disciplina,
    Entrenador,
    Entrenadores_Disciplina,
    Ejercicio,
    Disciplina,
    Microciclo,
    Entrenadores_Microciclo,
    Dia_Entrenamiento
)

# Renderiza la página de inicio.
def get_pagina_inicio(request):
    return render(
        request,
        'inicio.html',
        {}
    )

# Vista que muestra a todos los atletas registrados en la base de datos.
class ListaAtletas(ListView):
    model = Atleta
    template_name = 'entrenamientos/lista/atletas.html'

# Vista que muestra a todos los entrenadores registrados en la base de datos.
class ListaEntrenadores(ListView):
    model = Entrenador
    template_name = 'entrenamientos/lista/entrenadores.html'

# Vista que muestra a todas las disciplinas registradas en la base de datos.
class ListaDisciplinas(ListView):
    model = Disciplina
    template_name = 'entrenamientos/lista/disciplinas.html'

# Vista que muestra a todos los ejercicios registrados en la base de datos.
class ListaEjercicios(ListView):
    model = Ejercicio
    template_name = 'entrenamientos/lista/ejercicios.html'

# Vista que muestra la información de un atleta.
class VistaDetalleAtleta(DetailView):
    model = Atleta
    template_name = 'entrenamientos/detalle/atleta.html'

# Vista que muestra la información de un entrenador.
class DetalleEntrenador(DetailView):
    model = Entrenador
    template_name = 'entrenamientos/detalle/entrenador.html'

# Vista que muestra los microciclos
class ListaMicrociclos():
    def get_vista(request, pk):
        atleta = Atleta.objects.get(pk=pk)
        microciclos = Microciclo.objects.filter(atleta_fk=atleta)

        context = {
            'atleta': atleta,
            'microciclos': microciclos
        }

        return render(
            request,
            'entrenamientos/lista/microciclos_atleta.html',
            context
        )

# Vista que muestra los días de entrenamiento de un microciclo de un atleta.
class ListaDiasEntrenamiento(ListView):
    model = Dia_Entrenamiento
    template_name = 'entrenamientos/lista/dias_entrenamiento.html'

    def get_context_data(**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ListaDiasEntrenamiento():
    def get_vista(request, pk1, pk2):
        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=pk1)

        # Obtener el microciclo del atleta.
        microciclo = Microciclo.objects.get(pk=pk2)

        # Obtener los días de entrenamiento del microciclo.
        dias_entrenamiento = Dia_Entrenamiento.objects.filter(microciclo_fk=microciclo)

        context = {
            'dias_entrenamiento': dias_entrenamiento,
            'atleta': atleta,
            'microciclo': microciclo,
        }

        return render(
            request,
            'entrenamientos/lista/dias_entrenamiento.html',
            context
        )

# Vista que muestra la información de una disciplina.
class DetalleDisciplina(DetailView):
    model = Disciplina
    template_name = 'entrenamientos/detalle/disciplina.html'

# Vista que muestra la información de un ejercicio.
class DetalleEjercicio(DetailView):
    model = Ejercicio
    template_name = 'entrenamientos/detalle/ejercicio.html'

# Vista para agregar un ejercicio.
class AgregarEjercicio(CreateView):
    model = Ejercicio
    template_name ='entrenamientos/formulario/agregar_ejercicio.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('lista_ejercicios')

# Vista para agregar una disciplina.
class AgregarDisciplina(CreateView):
    model = Disciplina
    template_name = 'entrenamientos/formulario/agregar_disciplina.html'
    fields = '__all__'
    success_url = reverse_lazy('lista_disciplinas')

# Vista para agregar un atleta nuevo.
class AgregarAtleta(FormView):
    form_class = FormularioPersona
    template_name = 'entrenamientos/formulario/agregar_atleta.html'
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        form.agregar_atleta(self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # form = FormularioPersona()
        # form.es_entrenador_atleta(bandera = 'Atleta')
        # form.set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        context['form'].set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        context['disciplinas'] = Disciplina.objects.count()
        return context

# Vista para agregar un entrenador nuevo.
class AgregarEntrenador(FormView):
    form_class = FormularioPersona
    template_name = 'entrenamientos/formulario/agregar_entrenador.html'
    success_url = reverse_lazy('lista_entrenadores')

    def form_valid(self, form):
        form.agregar_entrenador(self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FormularioPersona()
        form.es_entrenador_atleta(bandera = 'Entrenador')
        form.set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        context['form'] = form
        return context

# Vista para agregar a un entrenador como atleta.
class AgregarAtletaExistente():
    def get_form(request):
        # Creación del formulario.
        form = FormularioPersonaExistente()

        entrenadores = [] # Lista para almacenar entrenadores.
        personas = []     # Lista para almacenar entrenadores que no están registrados como atletas.
        atletas = []      # Lista para almacenar atletas.

        # Guardar todos los atletas registrados en la lista atletas.
        for a in Atleta.objects.all():
            atletas.append(a.persona_fk)

        # Guardar todos los entrenadores registrados en la lista entrenadores.
        for e in Entrenador.objects.all():
            entrenadores.append(e.persona_fk)

            # Verificar si el entrenador no está registrado en la tabla de atletas. Si no lo
            # está, agregarlo a la lista de personas (lista que se usará como select para el
            # formulario).
            if not atletas.count(e.persona_fk):
                tupla = (e.persona_fk.pk, e.__str__())
                personas.append(tupla)

        # Establecer la lista personas como select del formulario.
        form.set_personas(personas=personas)

        # Cada disciplina existente en la base de datos, se añadirá como checkbox en el formulario.
        form.set_disciplinas(disciplinas=Disciplina.get_queryset_tupla_disciplinas())

        context = {
            'form': form.es_entrenador_atleta('Atleta'),
        }

        return render(
            request,
            'entrenamientos/formulario/agregar_atleta_existente.html',
            context
        )

    def agregar_atleta(request):
        # Obtener los datos del formulario.
        persona_id = request.POST['personas']
        disciplinas = request.POST.getlist('disciplinas')

        # Obtener a la persona mediante su llave primaria.
        persona = Persona.objects.get(pk=persona_id)

        # Creación de un objeto Atleta, el cuál obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Atleta.
        atleta = Atleta(persona_fk=persona)
        atleta.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla
        # Atletas_Disciplina, con la información del atleta y de la disciplina.
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                atleta_disciplina = Atletas_Disciplina(
                    atleta_fk = atleta,
                    disciplina_fk = disciplina
                )

                atleta_disciplina.save()
                contador += 1
            else:
                contador += 1
        return HttpResponseRedirect(reverse_lazy('lista_atletas'))

# Vista para agregar un atleta como entrenador.
class AgregarEntrenadorExistente():
    def get_form(request):
        # Creación del formulario.
        form = FormularioPersonaExistente()

        entrenadores = [] # Lista para almacenar entrenadores.
        atletas = []      # Lista para almacenar atletas.
        personas = []     # Lista para almacenar entrenadores que no están registrados como atletas.

        # Guardar todos los entrenadores registrados en la lista entrenadores.
        for e in Entrenador.objects.all():
            entrenadores.append(e.persona_fk)

        # Guardar todos los atletas registrados en la lista atletas.
        for a in Atleta.objects.all():
            atletas.append(a.persona_fk)

            # Verificar si el atleta no está registrado en la tabla de entrenadores. Si no lo
            # está, agregarlo a la lista de personas (lista que se usará como select para el
            # formulario).
            if not entrenadores.count(a.persona_fk):
                tupla = (a.persona_fk.pk, a.__str__())
                personas.append(tupla)

        # Establecer la lista personas como select del formulario.
        form.set_personas(personas=personas)

        # Cada disciplina existente en la base de datos, se añadirá como checkbox en el formulario.
        form.set_disciplinas(disciplinas=Disciplina.get_queryset_tupla_disciplinas())

        context = {
            'form': form.es_entrenador_atleta('Entrenador'),
        }

        return render(
            request,
            'entrenamientos/formulario/agregar_entrenador_existente.html',
            context
        )

    def agregar_entrenador(request):
        # Obtener los datos del formulario.
        persona_id = request.POST['personas']
        disciplinas = request.POST.getlist('disciplinas')

        # Obtener a la persona mediante su llave primaria.
        persona = Persona.objects.get(pk=persona_id)

        # Creación de un objeto Entrenador, el cuál obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Entrenadores.
        entrenador = Entrenador(persona_fk=persona)
        entrenador.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla
        # Entrenadores_Disciplina, con la información del entrenador y de la disciplina.
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                entrenador_disciplina = Entrenadores_Disciplina(
                    entrenador_fk = entrenador,
                    disciplina_fk = disciplina
                )

                entrenador_disciplina.save()
                contador += 1
            else:
                contador += 1
        return HttpResponseRedirect(reverse_lazy('lista_entrenadores'))

# Vista para agregar un microciclo
class AgregarMicrociclo():
    def get_form(request, pk):
        # Obtener al atleta por su llave primaria.
        atleta = Atleta.objects.get(pk=pk)

        # Creación del formulario
        form = FormularioMicrociclo()

        # Agregar como checkboxes los entrenadores registrados.
        form.set_entrenadores(entrenadores=Entrenador.get_queryset_tupla_entrenadores())

        context = {
            'form': form,
            'atleta': atleta
        }

        return render(
            request,
            'entrenamientos/formulario/agregar_microciclo.html',
            context
        )

    def agregar_microciclo(request, pk):
        # Obtener datos del formulario.
        titulo = request.POST['titulo']
        entrenadores = request.POST.getlist('entrenadores')

        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=pk)

        # Creación de un nuevo objeto Microciclo.
        microciclo = Microciclo()
        microciclo.titulo = titulo
        microciclo.numero_microciclo = Microciclo.objects.filter(atleta_fk=atleta).count() + 1
        microciclo.atleta_fk = atleta

        # Guardar microciclo en la base de datos.
        microciclo.save()

        contador = 1 # Variable para recorres la lista de checkboxes de los entrenadores.

        # Por cada checkbox de entrenadores seleccionado, se agrega un registro en la tabla
        # Entrenadores_Microciclo, con la información del entrenador y del microciclo.
        for entrenador in Entrenador.get_queryset_entrenadores():
            if entrenadores.count(f'{contador}') == 1:
                entrenador_microciclo = Entrenadores_Microciclo(
                    entrenador_fk = entrenador,
                    microciclo_fk = microciclo
                )

                entrenador_microciclo.save()
                contador += 1
            else:
                contador += 1
        return HttpResponseRedirect(reverse_lazy('microciclos_atleta', kwargs={'pk': pk}))

# Vista para añadir un día de entrenamiento a un microciclo en específico.
class AgregarDia():
    def get_form(request, pk1, pk2):
        # Obtener al atleta y al microciclo mediante sus llaves primarias.
        atleta = Atleta.objects.get(pk=pk1)
        microciclo = Microciclo.objects.get(pk=pk2)

        context = {
            'form': FormularioDiaEntrenamiento(),
            'atleta': atleta,
            'microciclo': microciclo,
        }

        return render(
            request,
            'entrenamientos/formulario/agregar_dia.html',
            context
        )

    def agregar_dia(request, pk1, pk2):
        # Obtener datos del formulario.
        titulo = request.POST['titulo']

        # Obtener el microciclo mediante su llave primaria.
        microciclo = Microciclo.objects.get(pk=pk2)

        # Creación de un objeto Dia_Entrenamiento
        dia_entrenamiento = Dia_Entrenamiento()
        dia_entrenamiento.titulo = titulo
        dia_entrenamiento.microciclo_fk = microciclo

        # Guardarlo en la base de datos.
        dia_entrenamiento.save()
        return HttpResponseRedirect(reverse_lazy('dias_entrenamiento', kwargs={'pk1': pk1, 'pk2': pk2}))

# Vista para agregar un ejercicio a un día de entrenamiento
class AgregarEjercicioDia():
    def get_form(request, pk1, pk2, pk3):
        # Obtener al atleta, microciclo y el día de entrenamiento mediante sus llaves primarias.
        atleta = Atleta.objects.get(pk=pk1)
        microciclo = Microciclo.objects.get(pk=pk2)
        dia_entrenamiento = Dia_Entrenamiento.objects.get(pk=pk3)

        context = {
            'form': FormularioEjercicio(),
            'atleta': atleta,
            'microciclo': microciclo,
            'dia_entrenamiento': dia_entrenamiento,
        }

        return render(
            request,
            'entrenamientos/formulario/agregar_ejercicio_dia.html',
            context
        )

    def agregar_ejercicio(request, pk1, pk2, pk3):
        dia_entrenamiento = Dia_Entrenamiento.objects.get(pk=pk3)

        # Obtener los datos del formulario.
        ejercicio_pk = request.POST['ejercicios_fk']
        series = request.POST['series']
        repeticiones = request.POST['repeticiones']
        escala = request.POST['escala']
        intensidad = request.POST['intensidad']
        peso_kg = request.POST['peso_kg']

        # Obtener el ejercicio mediante la llave primaria que nos da el select.
        ejercicio = Ejercicio.objects.get(pk=ejercicio_pk)

        # Creación de un objeto Dias_Ejercicios.
        dias_ejercicios = Dias_Ejercicios()
        dias_ejercicios.dias_entrenamiento_fk = dia_entrenamiento
        dias_ejercicios.ejercicios_fk = ejercicio
        dias_ejercicios.series = series
        dias_ejercicios.repeticiones = repeticiones
        dias_ejercicios.escala = escala
        dias_ejercicios.intensidad = intensidad
        dias_ejercicios.peso_kg = peso_kg

        # Guardar en la base de datos.
        dias_ejercicios.save()
        return HttpResponseRedirect(reverse_lazy('dias_entrenamiento', kwargs={'pk1': pk1, 'pk2': pk2,}))

# Vista para editar información de un ejercicio.
class EditarEjercicio(UpdateView):
    model = Ejercicio
    template_name = 'entrenamientos/formulario/editar_ejercicio.html'
    fields = '__all__'

# Vista para editar información de una disciplina.
class EditarDisciplina(UpdateView):
    model = Disciplina
    template_name = 'entrenamientos/formulario/editar_disciplina.html'
    fields = '__all__'
    success_url = reverse_lazy('lista_disciplinas')

# Vista para editar la información de un atleta.
class EditarAtleta():
    def get_form(request, pk):
        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=pk)

        # Creación del formulario.
        form = FormularioPersona()

        # Llenar el formulario con los datos del atleta.
        form.set_nombre(atleta.get_nombre())
        form.set_apellido(atleta.get_apellido())
        form.set_edad(atleta.get_edad)

        # Agregar como checkboxes al formulario todas las disciplinas que están registradas.
        form.set_disciplinas(disciplinas=Disciplina.get_queryset_tupla_disciplinas())

        context = {
            'form': form.es_entrenador_atleta('Atleta'),
            'atleta': atleta,
        }

        return render(
            request,
            'entrenamientos/formulario/editar_atleta.html',
            context
        )

    def editar_atleta(request, pk):
        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=pk)

        # Obtener a la persona en base a la información del atleta.
        persona = Persona.objects.get(pk=atleta.persona_fk.pk)

        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas')

        # Actualizar los datos de la persona.
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Actualizar el registro.
        persona.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Recorrido de la lista de checkboxes. Verifica cúales están seleccionados, y cuáles
        # no. Para todo checkbox seleccionado, se busca en la tabla Atletas_Disciplina si existe
        # un registro con la información del atleta y la disciplina. Si no existe, entonces, se crea
        # un nuevo registro en la tabla Atletas_Disciplina, caso contrario, si ya existe, omite el paso
        # anterior. Para todo checkbox no seleccionado, se busca en la tabla Atletas_Disciplina si existe
        # un registro con la información del atleta y la disciplina. Si existe, entonces, se elimina el
        # registro en la tabla Atletas_Disciplina, caso contrario, si no existe, omite el paso anterior.
        # Todo lo anterior se puede interpretar como: ¿Cuáles son las nuevas disciplinas que el atleta
        # entrena, y cuáles ha dejado de entrenar?
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                try:
                    atleta.atletas_disciplina_set.get(disciplina_fk=disciplina)
                except Atletas_Disciplina.DoesNotExist:
                    atleta.atletas_disciplina_set.create(atleta_fk=atleta, disciplina_fk=disciplina)
                else:
                    pass
                contador += 1
            else:
                try:
                    atleta.atletas_disciplina_set.get(disciplina_fk=disciplina)
                except Atletas_Disciplina.DoesNotExist:
                    pass
                else:
                    Atletas_Disciplina.objects.get(atleta_fk=atleta, disciplina_fk=disciplina).delete()
                contador += 1
        return HttpResponseRedirect(reverse_lazy('lista_atletas'))

# Vista para editar la información de un entrenador.
class EditarEntrenador():
    def get_form(request, pk):
        # Obtener al entrenador mediante su llave primaria.
        entrenador = Entrenador.objects.get(pk=pk)

        # Creación del formulario.
        form = FormularioPersona()

        # Llenar el formulario con los datos del entrenador.
        form.set_nombre(entrenador.get_nombre())
        form.set_apellido(entrenador.get_apellido())
        form.set_edad(entrenador.get_edad)

        # Agregar como checkboxes al formulario todas las disciplinas que están registradas.
        form.set_disciplinas(disciplinas=Disciplina.get_queryset_tupla_disciplinas())

        context = {
            'form': form.es_entrenador_atleta('Entrenador'),
            'entrenador': entrenador,
        }

        return render(
            request,
            'entrenamientos/formulario/editar_entrenador.html',
            context
        )

    def editar_entrenador(request, pk):
        # Obtener al entrenador mediante su llave primaria.
        entrenador = Entrenador.objects.get(pk=pk)

        # Obtener a la persona en base a la información del entrenador.
        persona = Persona.objects.get(pk=entrenador.persona_fk.pk)

        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas')

        # ACtualiza los datos de la persona.
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Actualizar el registro.
        persona.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Recorrido de la lista de checkboxes. Verifica cuáles están seleccionados, y cuáles
        # no. Para todo checkbox seleccionado, se busca en la tabla Entrenadores_Disciplina si existe
        # un registro con la información del entrenador y la disciplina. Si no existe, entonces, se crea
        # un nuevo registro en la tabla Entrenadores_Disciplina, caso contrario, si ya existe,omite el paso
        # anterior. Para todo checkbox no seleccionado, se busca en la tabla Entrenadores_Disciplina si existe
        # un registro con la información del entrenador y la disciplina. Si existe, entonces, se elimina el
        # registro en la tabla Entrenadores_Disciplina, caso contrario, si no existem omite el paso anterior.
        # Todo lo anterior se puede interpretar como: ¿Cuáles son las nuevas disciplinas que el entrenador
        # imparte, y cuáles ha dejado de impartir?
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                try:
                    entrenador.entrenadores_disciplina_set.get(disciplina_fk=disciplina)
                except Entrenadores_Disciplina.DoesNotExist:
                    entrenador.entrenadores_disciplina_set.create(entrenador_fk=entrenador, disciplina_fk=disciplina)
                else:
                    pass
                contador += 1
            else:
                try:
                    entrenador.entrenadores_disciplina_set.get(disciplina_fk=disciplina)
                except Entrenadores_Disciplina.DoesNotExist:
                    pass
                else:
                    Entrenadores_Disciplina.objects.get(entrenador_fk=entrenador, disciplina_fk=disciplina).delete()
                contador += 1
        return HttpResponseRedirect(reverse_lazy('lista_entrenadores'))

# Vista que modifica la información de un día de entrenamiento
class EditarDia(UpdateView):
    model = Dia_Entrenamiento
    template_name = 'entrenamientos/formulario/editar_dia.html'
    fields = ['titulo']

# Vista para editar la información de un microciclo
class EditarMicrociclo(UpdateView):
    model = Microciclo
    template_name = 'entrenamientos/formulario/editar_microciclo.html'
    fields = ['titulo']

# Vista para editar la información de un ejercicio en un día de entrenamiento.
class EditarEjercicioDia(UpdateView):
    model = Dias_Ejercicios
    template_name = 'entrenamientos/formulario/editar_ejercicio_dia.html'
    fields = ['ejercicios_fk', 'series', 'repeticiones', 'escala', 'intensidad', 'peso_kg']

# Vista para eliminar un atleta sin borrar el registro de la persona de
# la base de datos.
class EliminarAtleta(DeleteView):
    model = Atleta
    template_name = 'entrenamientos/formulario/eliminar_atleta.html'
    success_url = reverse_lazy('lista_atletas')

# Vista para eliminar un entrenador sin borrar el regitro de la persona de
# la base de datos.
class EliminarEntrenador(DeleteView):
    model = Entrenador
    template_name = 'entrenamientos/formulario/eliminar_entrenador.html'
    success_url = reverse_lazy('lista_entrenadores')

# Vista para eliminar por completo el registro de un entrenador y/o atleta
# de la base de datos.
class EliminarPersona(DeleteView):
    model = Persona
    template_name = 'entrenamientos/formulario/eliminar_persona.html'
    success_url = reverse_lazy('inicio')

# Vista para eliminar un ejercicio.
class EliminarEjercicio(DeleteView):
    model = Ejercicio
    template_name = 'entrenamientos/formulario/eliminar_ejercicio.html'
    success_url = reverse_lazy('lista_ejercicios')

# Vista para eliminar una disciplina.
class EliminarDisciplina(DeleteView):
    model = Disciplina
    template_name = 'entrenamientos/formulario/eliminar_disciplina.html'
    success_url = reverse_lazy('lista_disciplinas')

# Vista para eliminar un microciclo.
class EliminarMicrociclo(DeleteView):
    model = Microciclo
    template_name = 'entrenamientos/formulario/eliminar_microciclo.html'
    success_url = reverse_lazy('lista_atletas')

# Vista para eliminar un día de entrenamiento.
class EliminarDia(DeleteView):
    model = Dia_Entrenamiento
    template_name = 'entrenamientos/formulario/eliminar_dia.html'
    success_url = reverse_lazy('lista_atletas')

# Vista para eliminar un ejercicio de un día de entrenamiento.
class EliminarEjercicioDia(DeleteView):
    model = Dias_Ejercicios
    template_name = 'entrenamientos/formulario/eliminar_ejercicio_dia.html'
    success_url = reverse_lazy('lista_atletas')

# Vistas para hacer peticiones desde el FrontEnd. Las respuestas serán
# enviadas como un JSON.

# Obtener las disciplinas que entrena un atleta.
def atletas_disciplinas(request, pk):
    atleta = Atleta.objects.get(pk=pk)
    disciplinas = Atletas_Disciplina.objects.filter(atleta_fk=atleta)
    diccionario = {}
    contador = 1
    for d in disciplinas:
        diccionario[f'{contador}'] = d.disciplina_fk.nombre
        contador += 1

    return HttpResponse(json.dumps(diccionario))

# Obtener las disciplinas que imparte un entrenador.
def entrenadores_disciplinas(request, pk):
    entrenador = Entrenador.objects.get(pk=pk)
    disciplinas = Entrenadores_Disciplina.objects.filter(entrenador_fk=entrenador)
    diccionario = {}
    contador = 1

    for d in disciplinas:
        diccionario[f'{contador}'] = d.disciplina_fk.nombre
        contador += 1

    return HttpResponse(json.dumps(diccionario))

# Obtener el sexo de una persona.
def persona_sexo(request, pk):
    persona = Persona.objects.get(pk=pk)
    diccionario = {
        'sexo': persona.sexo,
    }

    return HttpResponse(json.dumps(diccionario))