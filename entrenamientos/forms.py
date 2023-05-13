from django import forms
from django.forms import ModelForm
from .models import Disciplina, Persona, Atleta, Entrenador, Dias_Ejercicios

# Formulario para agregar atletas y/o entrenadores no registrados en la base de datos.
class FormularioPersona(forms.Form):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'nombre'
            }
        ),
        label='Nombre',
        required=True,

    )


    apellido = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'apellido',
            }
        ),
        label='Apellido',
        required=True,
    )

    edad = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'id': 'edad',
            }
        ),
        label='Edad',
        required=True,
    )

    sexo = forms.CharField(
        widget=forms.Select(
            choices=Persona.SEXOS,
            attrs={
                'id': 'sexo',
            }
        ),
        label='Sexo',
        required=True,
    )

    fotografia = forms.CharField(
        widget=forms.FileInput(
            attrs={
                'id': 'fotografia',
            }
        ),
        label='Fotografía',
        required=False,
    )

    disciplinas = forms.CharField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'id': 'disciplinas'
            }
        ),
        required=True,
    )

    def es_entrenador_atleta(self, bandera):
        if bandera == 'Entrenador':
            # Acceso a los campos de un formulario
            self.fields['disciplinas'].label = 'Disciplina(s) que imparte'
        else:
            self.fields['disciplinas'].label = 'Disciplina(s) que practica'
        return self

    def set_disciplinas(self, disciplinas):
        self.fields['disciplinas'].widget.choices=disciplinas

    # Funciones que se mandan a llamar para editar la información de la persona
    def set_nombre(self, nombre):
        self.fields['nombre'].widget.attrs['value'] = nombre

    def set_apellido(self, apellido):
        self.fields['apellido'].widget.attrs['value'] = apellido

    def set_edad(self, edad):
        self.fields['edad'].widget.attrs['value'] = edad

    def set_sexo(self, sexo):
        self.fields['sexo'].widget.attrs['selected'] = sexo

# Formulario para agregar atletas y entrenadores con personas ya registradas en la base de datos.
class FormularioPersonaExistente(forms.Form):
    personas = forms.CharField(
        widget=forms.Select(
            attrs={
                'id': 'personas',
            }
        ),
        label='Personas registradas',
        required=True,
    )

    disciplinas = forms.CharField(
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'id': 'disciplinas'
            }
        ),
        required=True
    )

    # Funciones para el manejo del formulario
    def set_personas(self, personas):
        self.fields['personas'].widget.choices=personas

    def set_disciplinas(self, disciplinas):
        self.fields['disciplinas'].widget.choices=disciplinas

    def es_entrenador_atleta(self, bandera):
        if bandera == 'Entrenador':
            self.fields['disciplinas'].label = 'Disciplina(s) que imparte'
        else:
            self.fields['disciplinas'].label = 'Disciplina(s) que practica'
        return self

# Formulario para agregar microciclos
class FormularioMicrociclo(forms.Form):
    titulo = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'id': 'titulo'
            }
        ),
        label = 'Título',
        required = True
    )

    entrenadores = forms.CharField(
        widget = forms.CheckboxSelectMultiple(
            attrs = {
                'id': 'entrenadores'
            }
        ),
        label = 'Entrenador(es) que planifica(n) el microciclo',
        required = True
    )

    def set_entrenadores(self, entrenadores):
        self.fields['entrenadores'].widget.choices = entrenadores

# Formulario para agregar un día de entrenamiento a un microciclo.
class FormularioDiaEntrenamiento(forms.Form):
    titulo = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'id': 'titulo'
            }
        ),
        label = 'Título',
        required = True
    )

# Formulario para agregar un ejercicio a un día de entrenamiento
class FormularioEjercicio(ModelForm):
    class Meta():
        model = Dias_Ejercicios
        fields = ['ejercicios_fk', 'series', 'repeticiones', 'escala', 'intensidad', 'peso_kg']