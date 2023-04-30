from django.urls import path
from .views import *

urlpatterns = [
    path('', get_pagina_inicio, name='inicio'),
    path('atletas/', VistaListaAtletas.as_view(), name='lista_atletas'),
    path('atletas/<int:atleta_pk>/', VistaDetalleAtleta.get_vista, name='detalle_atleta'),
    path('entrenadores/', VistaListaEntrenadores.as_view(), name='lista_entrenadores'),
    path('entrenadores/<int:entrenador_pk>/', VistaDetalleEntrenador.get_vista, name='detalle_entrenador'),
    path('disciplinas/', VistaListaDisciplinas.as_view(), name='lista_disciplinas'),
    path('disciplinas/<int:pk>/', VistaDetalleDisciplina.as_view(), name='detalle_disciplina'),
    path('ejercicios/', VistaListaEjercicios.as_view(), name='lista_ejercicios'),
    path('ejercicios/<int:pk>/', VistaDetalleEjercicio.as_view(), name='detalle_ejercicio'),
]