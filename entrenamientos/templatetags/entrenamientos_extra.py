from django import template
from django.contrib.auth.models import Group
from entrenamientos.models import (
    Dias_Ejercicios,
    Atletas_Disciplina,
    Entrenadores_Disciplina
)

register = template.Library()

# Etiqueta personalizada para cargar los ejercicios de un día de entrenamiento
# pertenecientes a un microciclo de un atleta.
@register.inclusion_tag('etiquetas/dias_ejercicios.html')
def dias_ejercicios(dia, user):
    dias_ejercicios = Dias_Ejercicios.objects.filter(dias_entrenamiento_fk=dia)
    return {
        'dias_ejercicios': dias_ejercicios,
        'user': user,
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

# Etiqueta personalizada para verificar si una persona es atleta.
@register.simple_tag
def es_atleta(usuario):
    grupo = Group.objects.get(name = 'Atleta')

    if grupo in usuario.groups.all():
        return True
    else:
        return False
    
# Etiqueta personalizada para verificar si una persona es entrenador.
@register.simple_tag
def es_entrenador(usuario):
    grupo = Group.objects.get(name = 'Entrenador')

    if grupo in usuario.groups.all():
        return True
    else:
        return False