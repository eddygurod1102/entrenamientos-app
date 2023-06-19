from django.urls import path
from .views import *

urlpatterns = [
    # Página de inicio
    path('', get_pagina_inicio, name='inicio'),

    # URLs relacionados con atletas
    path('atletas/', ListaAtletas.as_view(), name='lista_atletas'),
    path('atletas/<int:pk>/', DetalleAtleta.as_view(), name='detalle_atleta'),
    path('atletas/nuevo/', AgregarAtleta.as_view(), name='agregar_atleta_nuevo'),
    path('atletas/existente/', AgregarAtletaExistente.as_view(), name='agregar_atleta_existente'),
    path('atletas/<int:pk>/editar/', EditarAtleta.as_view(), name='editar_atleta'),
    path('atletas/<int:pk>/eliminar/', EliminarAtleta.as_view(), name='eliminar_atleta'),
    path('atletas/<int:pk>/microciclos/', ListaMicrociclos.as_view(), name='microciclos_atleta'),
    path('atletas/microciclos/<int:pk>/editar/', EditarMicrociclo.as_view(), name='editar_microciclo'),
    path('atletas/microciclos/<int:pk>/eliminar/', EliminarMicrociclo.as_view(), name='eliminar_microciclo'),
    path('atletas/<int:pk>/microciclos/nuevo/', AgregarMicrociclo.as_view(), name='agregar_microciclo'),
    path('atletas/<int:pk1>/microciclos/<int:pk2>/dias_entrenamiento/', ListaDiasEntrenamiento.as_view(), name='dias_entrenamiento'),
    path('atletas/<int:pk1>/microciclos/<int:pk2>/dias_entrenamiento/nuevo/', AgregarDia.as_view(), name='agregar_dia'),
    path('atletas/dias_entrenamiento/<int:pk>/editar/', EditarDia.as_view(), name='editar_dia'),
    path('atletas/dias_entrenamiento/<int:pk>/eliminar/', EliminarDia.as_view(), name='eliminar_dia'),
    path('atletas/<int:pk1>/microciclos/<int:pk2>/dias_entrenamiento/<int:pk3>/nuevo_ejercicio/', AgregarEjercicioDia.as_view(), name='agregar_ejercicio_dia'),
    path('atletas/dias_ejercicio/<int:pk>/editar/', EditarEjercicioDia.as_view(), name='editar_ejercicio_dia'),
    path('atletas/dias_ejercicio/<int:pk>/eliminar', EliminarEjercicioDia.as_view(), name='eliminar_ejercicio_dia'),

    # URLs relacionados con entrenadores
    path('entrenadores/', ListaEntrenadores.as_view(), name='lista_entrenadores'),
    path('entrenadores/<int:pk>/', DetalleEntrenador.as_view(), name='detalle_entrenador'),
    path('entrenadores/nuevo/', AgregarEntrenador.as_view(), name='agregar_entrenador_nuevo'),
    path('entrenadores/existente/', AgregarEntrenadorExistente.as_view(), name='agregar_entrenador_existente'),
    path('entrenadores/<int:pk>/editar/', EditarEntrenador.as_view(), name='editar_entrenador'),
    path('entrenadores/<int:pk>/eliminar/', EliminarEntrenador.as_view(), name='eliminar_entrenador'),
    path('entrenadores/<int:pk>/atletas/', MisAtletas.as_view(), name='mis_atletas'),

    # URL para eliminar a una persona por completo
    path('personas/<int:pk>/eliminar/', EliminarPersona.as_view(), name='eliminar_persona'),

    # URLs relacionados con disciplinas
    path('disciplinas/', ListaDisciplinas.as_view(), name='lista_disciplinas'),
    path('disciplinas/<int:pk>/', DetalleDisciplina.as_view(), name='detalle_disciplina'),
    path('disciplinas/nueva/', AgregarDisciplina.as_view(), name='agregar_disciplina'),
    path('disciplinas/<int:pk>/editar/', EditarDisciplina.as_view(), name='editar_disciplina'),
    path('disciplinas/<int:pk>/eliminar/', EliminarDisciplina.as_view(), name='eliminar_disciplina'),

    # URLs relacionados con ejercicios
    path('ejercicios/', ListaEjercicios.as_view(), name='lista_ejercicios'),
    path('ejercicios/<int:pk>/', DetalleEjercicio.as_view(), name='detalle_ejercicio'),
    path('ejercicios/nuevo/', AgregarEjercicio.as_view(), name='agregar_ejercicio'),
    path('ejercicios/<int:pk>/editar/', EditarEjercicio.as_view(), name='editar_ejercicio'),
    path('ejercicios/<int:pk>/eliminar/', EliminarEjercicio.as_view(), name='eliminar_ejercicio'),

    # URLs para interactuar con Javascript
    path('atletas_disciplinas/<int:pk>/', atletas_disciplinas, name='atletas_disciplinas'),
    path('entrenadores_disciplinas/<int:pk>/', entrenadores_disciplinas, name='entrenadores_disciplinas'),
    path('persona_sexo/<int:pk>/', persona_sexo, name='persona_sexo'),
]