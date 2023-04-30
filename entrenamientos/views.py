from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Atleta, Atletas_Disciplina, Entrenador, Entrenadores_Disciplina, Ejercicio, Disciplina

# Renderiza la página de inicio
def get_pagina_inicio(request):
    return render(
        request,
        'inicio.html',
        {}
    )

# Vista que muestra a todos los atletas registrados en la base de datos
class VistaListaAtletas(ListView):
    model = Atleta
    template_name = 'entrenamientos/lista_atletas.html'

# Vista que muestra a todos los entrenadores registrados en la base de datos
class VistaListaEntrenadores(ListView):
    model = Entrenador
    template_name = 'entrenamientos/lista_entrenadores.html'

# Vista que muestra a todas las disciplinas registradas en la base de datos
class VistaListaDisciplinas(ListView):
    model = Disciplina
    template_name = 'entrenamientos/lista_disciplinas.html'

# Vista que muestra a todos los ejercicios registrados en la base de datos
class VistaListaEjercicios(ListView):
    model = Ejercicio
    template_name = 'entrenamientos/lista_ejercicios.html'

# Vista que muestra la información de un atleta
class VistaDetalleAtleta():
    def get_vista(request, atleta_pk):
        atleta = Atleta.objects.get(pk=atleta_pk)
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
    
# Vista que muestra la información de un entrenador
class VistaDetalleEntrenador():
    def get_vista(request, entrenador_pk):
        entrenador = Entrenador.objects.get(pk=entrenador_pk)
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
    
# Vista que muestra la información de una disciplina
class VistaDetalleDisciplina(DetailView):
    model = Disciplina
    template_name = 'entrenamientos/detalle_disciplina.html'

# Vista que muestra la información de un ejercicio
class VistaDetalleEjercicio(DetailView):
    model = Ejercicio
    template_name = 'entrenamientos/detalle_ejercicio.html'