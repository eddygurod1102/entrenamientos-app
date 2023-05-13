from django import template
from entrenamientos.models import Dias_Ejercicios

register = template.Library()

# Etiqueta personalizada para cargar los ejercicios de un día de entrenamiento
# pertenecientes a un microciclo de un atleta.
@register.inclusion_tag('etiquetas/dias_ejercicios.html')
def dias_ejercicios(dia):
    dias_ejercicios = Dias_Ejercicios.objects.filter(dias_entrenamiento_fk=dia)
    return {
        'dias_ejercicios': dias_ejercicios,
    }