from django import template
from entrenamientos.models import (
    Dias_Ejercicios,
    Atletas_Disciplina,
    Entrenadores_Disciplina
)

register = template.Library()

# Etiqueta personalizada para cargar los ejercicios de un día de entrenamiento
# pertenecientes a un microciclo de un atleta.
@register.inclusion_tag('etiquetas/dias_ejercicios.html')
def dias_ejercicios(dia):
    dias_ejercicios = Dias_Ejercicios.objects.filter(dias_entrenamiento_fk=dia)
    return {
        'dias_ejercicios': dias_ejercicios,
    }

# Etiqueta personalizada para cargar las disciplinas que entrena un atleta.
@register.inclusion_tag('etiquetas/atleta_disciplinas.html')
def atleta_disciplinas(atleta):
    atleta_disciplinas = Atletas_Disciplina.objects.filter(atleta_fk=atleta)
    return {
        'atleta_disciplinas': atleta_disciplinas,
    }

# Etiqueta personalizada para cargar las disciplinas que imparte un entrenador.
@register.inclusion_tag('etiquetas/entrenador_disciplinas.html')
def entrenador_disciplinas(entrenador):
    entrenador_disciplinas = Entrenadores_Disciplina.objects.filter(entrenador_fk=entrenador)
    return {
        'entrenador_disciplinas': entrenador_disciplinas,
    }