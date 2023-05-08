from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
import json
from .forms import *
from .models import Atleta, Atletas_Disciplina, Entrenador, Entrenadores_Disciplina, Ejercicio, Disciplina

# Renderiza la página de inicio.
def get_pagina_inicio(request):
    return render(
        request,
        'inicio.html',
        {}
    )

# Vista que muestra a todos los atletas registrados en la base de datos.
class VistaListaAtletas(ListView):
    model = Atleta
    template_name = 'entrenamientos/lista_atletas.html'

# Vista que muestra a todos los entrenadores registrados en la base de datos.
class VistaListaEntrenadores(ListView):
    model = Entrenador
    template_name = 'entrenamientos/lista_entrenadores.html'

# Vista que muestra a todas las disciplinas registradas en la base de datos.
class VistaListaDisciplinas(ListView):
    model = Disciplina
    template_name = 'entrenamientos/lista_disciplinas.html'

# Vista que muestra a todos los ejercicios registrados en la base de datos.
class VistaListaEjercicios(ListView):
    model = Ejercicio
    template_name = 'entrenamientos/lista_ejercicios.html'

# Vista que muestra la información de un atleta.
class VistaDetalleAtleta():
    def get_vista(request, atleta_pk):
        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=atleta_pk)

        # Obtener las disciplinas que el atleta entrena.
        disciplinas = Atletas_Disciplina.objects.filter(atleta_fk=atleta)

        context = {
            'atleta': atleta,
            'disciplinas': disciplinas,
        }

        return render(
            request,
            'entrenamientos/detalle_atleta.html',
            context
        )
    
# Vista que muestra la información de un entrenador.
class VistaDetalleEntrenador():
    def get_vista(request, entrenador_pk):
        # Obtener al entrenador mediante su llave primaria.
        entrenador = Entrenador.objects.get(pk=entrenador_pk)

        # Obtener las disciplinas que el entrenador imparte.
        disciplinas = Entrenadores_Disciplina.objects.filter(entrenador_fk=entrenador)

        context = {
            'entrenador': entrenador,
            'disciplinas': disciplinas,
        }

        return render(
            request,
            'entrenamientos/detalle_entrenador.html',
            context
        )
    
# Vista que muestra la información de una disciplina.
class VistaDetalleDisciplina(DetailView):
    model = Disciplina
    template_name = 'entrenamientos/detalle_disciplina.html'

# Vista que muestra la información de un ejercicio.
class VistaDetalleEjercicio(DetailView):
    model = Ejercicio
    template_name = 'entrenamientos/detalle_ejercicio.html'

# Vista para agregar un ejercicio.
class VistaFormularioAgregarEjercicio(CreateView):
    model = Ejercicio
    template_name ='entrenamientos/formulario_agregar_ejercicio.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('lista_ejercicios')

# Vista para agregar una disciplina.
class VistaFormularioAgregarDisciplina(CreateView):
    model = Disciplina
    template_name = 'entrenamientos/formulario_agregar_disciplina.html'
    fields = '__all__'
    success_url = reverse_lazy('lista_disciplinas')

# Vista para agregar un atleta nuevo.
class VistaFormularioAgregarAtleta():
    def get_form(request):
        # Creación del formulario.
        form = FormularioPersona()

        # Agregar como checkboxes al formulario todas las disciplinas que están registradas.
        form.set_disciplinas(disciplinas=Disciplina.get_queryset_tupla_disciplinas())

        context = {
            'form': form.es_entrenador_atleta(bandera='Atleta')
        }

        return render(
            request,
            'entrenamientos/formulario_agregar_atleta.html',
            context
        )

    def agregar_atleta(request):
        # Obtener datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']

        # Obtiene lista de checkboxes activados.
        disciplinas = request.POST.getlist('disciplinas')

        # Creación de un nuevo objeto Persona.
        persona = Persona()
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Guardar el registro de la persona en la base de datos.
        persona.save()

        # Creación de un objeto Atleta, el cuál, obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Atletas.
        atleta = Atleta()
        atleta.persona_fk = persona
        atleta.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla 
        # Atletas_Disciplinas, con la información del atleta y de la disciplina.
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

# Vista para agregar un entrenador nuevo.
class VistaFormularioAgregarEntrenador():
    def get_form(request):
        # Creación del formulario.
        form = FormularioPersona()

        # Agregar como checkboxes al formulario todas las disciplinas que están registradas.
        form.set_disciplinas(disciplinas=Disciplina.get_queryset_tupla_disciplinas())

        context = {
            'form': form.es_entrenador_atleta(bandera='Entrenador')
        }

        return render(
            request,
            'entrenamientos/formulario_agregar_entrenador.html',
            context
        )

    def agregar_entrenador(request):
        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas') # Obtiene lista de checkboxes activados

        # Creación de un nuevo objeto Persona.
        persona = Persona()
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Guardar el registro de la persona en la base de datos.
        persona.save()

        # Creación de un objeto Entrenador, el cuál obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Entrenadores.
        entrenador = Entrenador()
        entrenador.persona_fk = persona
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


# Vista para agregar a un entrenador como atleta.
class VistaFormularioAgregarAtletaExistente():
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
            'entrenamientos/formulario_agregar_atleta_existente.html',
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
class VistaFormularioAgregarEntrenadorExistente():
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
            'entrenamientos/formulario_agregar_entrenador_existente.html',
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

# Vista para editar información de un ejercicio.
class VistaFormularioEditarEjercicio(UpdateView):
    model = Ejercicio
    template_name = 'entrenamientos/formulario_editar_ejercicio.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('lista_ejercicios')

# Vista para editar información de una disciplina.
class VistaFormularioEditarDisciplina(UpdateView):
    model = Disciplina
    template_name = 'entrenamientos/formulario_editar_disciplina.html'
    fields = '__all__'
    success_url = reverse_lazy('lista_disciplinas')

# Vista para editar la información de un atleta.
class VistaFormularioEditarAtleta():
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
            'entrenamientos/formulario_editar_atleta.html',
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
class VistaFormularioEditarEntrenador():
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
            'entrenamientos/formulario_editar_entrenador.html',
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



# Vista para eliminar un atleta sin borrar el registro de la persona de
# la base de datos.
class VistaFormularioEliminarAtleta(DeleteView):
    model = Atleta
    template_name = 'entrenamientos/formulario_eliminar_atleta.html'
    success_url = reverse_lazy('lista_atletas')

# Vista para eliminar un entrenador sin borrar el regitro de la persona de
# la base de datos.
class VistaFormularioEliminarEntrenador(DeleteView):
    model = Entrenador
    template_name = 'entrenamientos/formulario_eliminar_entrenador.html'
    success_url = reverse_lazy('lista_entrenadores')

# Vista para eliminar por completo el registro de un entrenador y/o atleta
# de la base de datos.
class VistaFormularioEliminarPersona(DeleteView):
    model = Persona
    template_name = 'entrenamientos/formulario_eliminar_persona.html'
    success_url = reverse_lazy('inicio')

# Vista para eliminar un ejercicio.
class VistaFormularioEliminarEjercicio(DeleteView):
    model = Ejercicio
    template_name = 'entrenamientos/formulario_eliminar_ejercicio.html'
    success_url = reverse_lazy('lista_ejercicios')

# Vista para eliminar una disciplina.
class VistaFormularioEliminarDisciplina(DeleteView):
    model = Disciplina
    template_name = 'entrenamientos/formulario_eliminar_disciplina.html'
    success_url = reverse_lazy('lista_disciplinas')


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