from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView
)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
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

# Vista que muestra los microciclos de un atleta
class ListaMicrociclos(ListView):
    model = Microciclo
    template_name = 'entrenamientos/lista/microciclos_atleta.html'
    context_object_name = 'microciclos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atleta'] = Atleta.objects.get(pk = self.kwargs['pk'])
        context['microciclos'] = Microciclo.objects.filter(atleta_fk = context['atleta'])
        return context

# Vista que muestra los días de entrenamiento de un microciclo de un atleta.
class ListaDiasEntrenamiento(ListView):
    model = Dia_Entrenamiento
    template_name = 'entrenamientos/lista/dias_entrenamiento.html'
    context_object_name = 'dias_entrenamiento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atleta'] = Atleta.objects.get(pk = self.kwargs['pk1'])
        context['microciclo'] = Microciclo.objects.get(pk = self.kwargs['pk2'])
        context['dias_entrenamiento'] = Dia_Entrenamiento.objects.filter(microciclo_fk = context['microciclo'])
        return context

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

    def form_valid(self, form):
        form.agregar_atleta(self.request)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        context['disciplinas'] = Disciplina.objects.count()
        return context
    
    def get_success_url(self):
        return reverse('lista_atletas')

# Vista para agregar un entrenador nuevo.
class AgregarEntrenador(FormView):
    form_class = FormularioPersona
    template_name = 'entrenamientos/formulario/agregar_entrenador.html'

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

    def get_success_url(self):
        return reverse('lista_entrenadores')

# Vista para agregar a un entrenador como atleta.
class AgregarAtletaExistente(FormView):
    form_class = FormularioPersonaExistente
    template_name = 'entrenamientos/formulario/agregar_atleta_existente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].set_personas(personas = Persona.get_lista_entrenadores())
        context['form'].set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        context['form'].es_entrenador_atleta('Atleta')
        return context
    
    def form_valid(self, form):
        form.agregar_atleta(self.request)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('lista_atletas')
    
# Vista para agregar a un atleta como entrenador.
class AgregarEntrenadorExistente(FormView):
    form_class = FormularioPersonaExistente
    template_name = 'entrenamientos/formulario/agregar_entrenador_existente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].set_personas(personas = Persona.get_lista_atletas())
        context['form'].set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        context['form'].es_entrenador_atleta('Entrenador')
        return context
    
    def form_valid(self, form):
        form.agregar_entrenador(self.request)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('lista_entrenadores')

# Vista para agregar un microciclo.
class AgregarMicrociclo(FormView):
    form_class = FormularioMicrociclo
    template_name = 'entrenamientos/formulario/agregar_microciclo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].set_entrenadores(entrenadores = Entrenador.get_queryset_tupla_entrenadores())
        context['atleta'] = Atleta.objects.get(pk = self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.agregar_microciclo(self.request, self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('microciclos_atleta', kwargs = {'pk': self.kwargs['pk']})

# Vista para añadir un día de entrenamiento a un microciclo en específico.
class AgregarDia(FormView):
    form_class = FormularioDiaEntrenamiento
    template_name = 'entrenamientos/formulario/agregar_dia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atleta'] = Atleta.objects.get(pk = self.kwargs['pk1'])
        context['microciclo'] = Microciclo.objects.get(pk = self.kwargs['pk2'])
        return context

    def form_valid(self, form):
        form.agregar_dia(self.request, self.kwargs['pk1'], self.kwargs['pk2'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('dias_entrenamiento', kwargs = {'pk1': self.kwargs['pk1'], 'pk2': self.kwargs['pk2']})
    
# Vista para agregar un ejercicio a un día de entrenamiento.
class AgregarEjercicioDia(FormView):
    form_class = FormularioEjercicio
    template_name = 'entrenamientos/formulario/agregar_ejercicio_dia.html'

    def form_valid(self, form):
        form.agregar_ejercicio(self.request, self.kwargs['pk3'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dias_entrenamiento', kwargs = {'pk1': self.kwargs['pk1'], 'pk2': self.kwargs['pk2']})

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
class EditarAtleta(FormView):
    form_class = FormularioEditarPersona
    template_name = 'entrenamientos/formulario/editar_atleta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atleta'] = Atleta.objects.get(pk = self.kwargs['pk'])
        context['form'].set_nombre(nombre = context['atleta'].persona_fk.nombre)
        context['form'].set_apellido(apellido = context['atleta'].persona_fk.apellido)
        context['form'].set_edad(edad = context['atleta'].persona_fk.edad)
        context['form'].set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        return context
    
    def form_valid(self, form):
        form.editar_atleta(self.request, self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detalle_atleta', kwargs = {'pk': self.kwargs['pk']})
    
# Vista para editar la información de un entrenador.
class EditarEntrenador(FormView):
    form_class = FormularioEditarPersona
    template_name = 'entrenamientos/formulario/editar_entrenador.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entrenador'] = Entrenador.objects.get(pk = self.kwargs['pk'])
        context['form'].set_nombre(nombre = context['entrenador'].persona_fk.nombre)
        context['form'].set_apellido(apellido = context['entrenador'].persona_fk.apellido)
        context['form'].set_edad(edad = context['entrenador'].persona_fk.edad)
        context['form'].set_disciplinas(disciplinas = Disciplina.get_queryset_tupla_disciplinas())
        return context

    def form_valid(self, form):
        form.editar_entrenador(self.request, self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detalle_entrenador', kwargs = {'pk': self.kwargs['pk']})

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

# -------------------------------------------------------------------------------------------------

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