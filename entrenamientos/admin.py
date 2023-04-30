from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Persona)
admin.site.register(Atleta)
admin.site.register(Entrenador)
admin.site.register(Disciplina)
admin.site.register(Ejercicio)
admin.site.register(Microciclo)
admin.site.register(Dia_Entrenamiento)
admin.site.register(Atletas_Disciplina)
admin.site.register(Entrenadores_Disciplina)
admin.site.register(Dias_Ejercicios)
admin.site.register(Entrenadores_Microciclo)