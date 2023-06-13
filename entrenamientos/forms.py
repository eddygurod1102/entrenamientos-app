from django import forms
from django.forms import ModelForm
from .models import Disciplina, Persona, Atleta, Entrenador, Dias_Ejercicios, Atletas_Disciplina, Entrenadores_Disciplina

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
            },
            choices = Disciplina.get_queryset_tupla_disciplinas()
        ),
        required = True,
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

    def agregar_atleta(self, request):
        # Obtener datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['apellido']
        fotografia = request.POST['fotografia']

        # Obtiene la lista de checkboxes activados.
        disciplinas = request.POST.getlist('disciplinas')

        # Creación de un nuevo objeto Persona.
        persona = Persona()
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Guardar el registro de la persona en la base de datos.
        persona.save()

        # Creación de un objeto Atleta, el cuál, obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Atletas.
        atleta = Atleta()
        atleta.persona_fk = persona
        atleta.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla 
        # Atletas_Disciplinas, con la información del atleta y de la disciplina.
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                atleta_disciplina = Atletas_Disciplina(
                    atleta_fk = atleta,
                    disciplina_fk = disciplina
                )

                atleta_disciplina.save()
                contador += 1
            else:
                contador += 1

    def agregar_entrenador(self, request):
        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas') # Obtiene lista de checkboxes activados

        # Creación de un nuevo objeto Persona.
        persona = Persona()
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Guardar el registro de la persona en la base de datos.
        persona.save()

        # Creación de un objeto Entrenador, el cuál obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Entrenadores.
        entrenador = Entrenador()
        entrenador.persona_fk = persona
        entrenador.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla
        # Entrenadores_Disciplina, con la información del entrenador y de la disciplina.
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                entrenador_disciplina = Entrenadores_Disciplina(
                    entrenador_fk = entrenador,
                    disciplina_fk = disciplina
                )

                entrenador_disciplina.save()
                contador += 1
            else:
                contador += 1

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

# Formulario de prueba
class FormularioPrueba(forms.Form):
    nombre = forms.CharField(
        max_length = 255,
        widget = forms.TextInput(
            attrs = {
                'name': 'nombre'
            }
        )
    )

    def imprimir_nombre(self, request):
        print(request.POST['nombre'])
