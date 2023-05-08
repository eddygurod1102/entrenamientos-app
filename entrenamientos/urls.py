from django.urls import path
from .views import *

urlpatterns = [
    # Página de inicio
    path('', get_pagina_inicio, name='inicio'),

    # URLs relacionados con atletas
    path('atletas/', VistaListaAtletas.as_view(), name='lista_atletas'),
    path('atletas/<int:atleta_pk>/', VistaDetalleAtleta.get_vista, name='detalle_atleta'),
    path('atletas/nuevo/', VistaFormularioAgregarAtleta.get_form, name='agregar_atleta_nuevo'),
    path('atletas/nuevo/ok/', VistaFormularioAgregarAtleta.agregar_atleta, name='atleta_agregado'),
    path('atletas/existente/', VistaFormularioAgregarAtletaExistente.get_form, name='agregar_atleta_existente'),
    path('atletas/existente/ok/', VistaFormularioAgregarAtletaExistente.agregar_atleta, name='atleta_existente_agregado'),
    path('atletas/<int:pk>/editar/', VistaFormularioEditarAtleta.get_form, name='editar_atleta'),
    path('atletas/<int:pk>/editado/', VistaFormularioEditarAtleta.editar_atleta, name='atleta_editado'),
    path('atletas/<int:pk>/eliminar/', VistaFormularioEliminarAtleta.as_view(), name='eliminar_atleta'),

    # URLs relacionados con entrenadores
    path('entrenadores/', VistaListaEntrenadores.as_view(), name='lista_entrenadores'),
    path('entrenadores/<int:entrenador_pk>/', VistaDetalleEntrenador.get_vista, name='detalle_entrenador'),
    path('entrenadores/nuevo/', VistaFormularioAgregarEntrenador.get_form, name='agregar_entrenador_nuevo'),
    path('entrenadores/nuevo/ok/', VistaFormularioAgregarEntrenador.agregar_entrenador, name='entrenador_agregado'),
    path('entrenadores/existente/', VistaFormularioAgregarEntrenadorExistente.get_form, name='agregar_entrenador_existente'),
    path('entrenadores/existente/ok/', VistaFormularioAgregarEntrenadorExistente.agregar_entrenador, name='entrenador_existente_agregado'),
    path('entrenadores/<int:pk>/editar/', VistaFormularioEditarEntrenador.get_form, name='editar_entrenador'),
    path('entrenadores/<int:pk>/editado/', VistaFormularioEditarEntrenador.editar_entrenador, name='entrenador_editado'),
    path('entrenadores/<int:pk>/eliminar/', VistaFormularioEliminarEntrenador.as_view(), name='eliminar_entrenador'),

    # URL para eliminar a una persona por completo
    path('personas/<int:pk>/eliminar/', VistaFormularioEliminarPersona.as_view(), name='eliminar_persona'),

    # URLs relacionados con disciplinas
    path('disciplinas/', VistaListaDisciplinas.as_view(), name='lista_disciplinas'),
    path('disciplinas/<int:pk>/', VistaDetalleDisciplina.as_view(), name='detalle_disciplina'),
    path('disciplinas/nueva/', VistaFormularioAgregarDisciplina.as_view(), name='agregar_disciplina'),
    path('disciplinas/<int:pk>/editar/', VistaFormularioEditarDisciplina.as_view(), name='editar_disciplina'),
    path('disciplinas/<int:pk>/eliminar/', VistaFormularioEliminarDisciplina.as_view(), name='eliminar_disciplina'),

    # URLs relacionados con ejercicios
    path('ejercicios/', VistaListaEjercicios.as_view(), name='lista_ejercicios'),
    path('ejercicios/<int:pk>/', VistaDetalleEjercicio.as_view(), name='detalle_ejercicio'),
    path('ejercicios/nuevo/', VistaFormularioAgregarEjercicio.as_view(), name='agregar_ejercicio'),
    path('ejercicios/<int:pk>/editar/', VistaFormularioEditarEjercicio.as_view(), name='editar_ejercicio'),
    path('ejercicios/<int:pk>/eliminar/', VistaFormularioEliminarEjercicio.as_view(), name='eliminar_ejercicio'),

    # URLs para interactuar con Javascript
    path('atletas_disciplinas/<int:pk>/', atletas_disciplinas, name='atletas_disciplinas'),
    path('entrenadores_disciplinas/<int:pk>/', entrenadores_disciplinas, name='entrenadores_disciplinas'),
    path('persona_sexo/<int:pk>/', persona_sexo, name='persona_sexo'),
]