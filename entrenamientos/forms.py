from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from .models import (
    Disciplina,
    Persona,
    Atleta,
    Entrenador,
    Dias_Ejercicios,
    Atletas_Disciplina,
    Entrenadores_Disciplina
)
from .validators import *
from cuentas.models import Persona_Cuenta

# Formulario para agregar atletas y/o entrenadores no registrados en la base de datos.
class FormularioPersona(forms.Form):
    nombre = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'id': 'nombre',
                'class': 'form-control',
                'autocomplete': 'off',
                'name': 'nombre',
            }
        ),
        validators = [
            validar_nombre,
        ],
    )

    apellido = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'id': 'apellido',
                'class': 'form-control',
                'autocomplete': 'off',
                'name': 'apellido',
            }
        ),
        validators = [
            validar_apellido,
        ]
    )

    edad = forms.CharField(
        widget = forms.NumberInput(
            attrs = {
                'id': 'edad',
                'class': 'form-control',
                'name': 'edad',
                'autocomplete': 'off',
            }
        ),
        validators = [
            validar_edad,
        ]
    )

    sexo = forms.CharField(
        widget = forms.Select(
            choices = Persona.SEXOS,
            attrs = {
                'id': 'sexo',
            }
        ),
    )

    fotografia = forms.CharField(
        widget = forms.FileInput(
            attrs = {
                'id': 'fotografia',
                'class': 'form-control',
                'name': 'fotografia',
            }
        ),
        required = False,
        validators = [
            validar_fotografia,
        ]
    )

    disciplinas = forms.CharField(
        widget = forms.CheckboxSelectMultiple(
            attrs = {
                'id': 'disciplinas',
                'name': 'disciplinas',
                'class': 'form-check-input',
            },
        ),
    )

    nombre_usuario = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'id': 'usuario',
                'class': 'form-control',
                'autocomplete': 'off',
                'name': 'nombre_usuario',
            }
        ),
        validators = [
            validar_nombre_usuario,
        ],
    )

    correo = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'id': 'correo',
                'name': 'correo',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        ),
        validators = [
            validar_correo_electronico,
        ],
    )

    contrasena = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'id': 'contrasena',
                'name': 'contrasena',
                'class': 'form-control',
                'autocomplete': 'off',
            }
        ),
        help_text = 'La contraseña debe incluir al menos 8 caracteres',
        validators = [
            validar_contrasena,
        ]
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
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        usuario = request.POST['nombre_usuario']
        correo = request.POST['correo']
        contrasena = make_password(request.POST['contrasena'])

        # Obtiene la lista de checkboxes activados.
        disciplinas = request.POST.getlist('disciplinas')

        print(type(fotografia))

        # # Creación de un nuevo objeto Persona.
        # persona = Persona(
        #     nombre = nombre,
        #     apellido = apellido,
        #     edad = edad,
        #     sexo = sexo,
        #     fotografia = fotografia
        # )

        # # Guardar el registro de la persona en la base de datos.
        # persona.save()

        # # Creación de un objeto Atleta, el cuál, obtiene los datos del objeto persona, para luego
        # # después, guardarlo en la base de datos, pero ahora en la tabla Atletas.
        # atleta = Atleta(persona_fk = persona)
        # # atleta.persona_fk = persona
        # atleta.save()

        # contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla 
        # # Atletas_Disciplinas, con la información del atleta y de la disciplina.
        # for disciplina in Disciplina.get_queryset_disciplinas():
        #     if disciplinas.count(f'{contador}') == 1:
        #         atleta_disciplina = Atletas_Disciplina(
        #             atleta_fk = atleta,
        #             disciplina_fk = disciplina
        #         )

        #         atleta_disciplina.save()
        #         contador += 1
        #     else:
        #         contador += 1

        # # Creación de un uevo objeto User.
        # usuario = User(
        #     username = usuario,
        #     email = correo,
        #     password = make_password(contrasena)
        # )


        # # Guardar el registro del usuario en la base de datos.
        # usuario.save()

        # # Agregamos al usuario en el grupo de atletas.
        # usuario.groups.add(Group.objects.get(name = 'Atleta'))

        # # Creación de un nuevo objecto Persona_Cuenta. Recuerda: una persona sólo puede tener
        # # una cuenta.
        # persona_cuenta = Persona_Cuenta(
        #     persona_fk = persona,
        #     usuario_fk = usuario
        # )

        # # Guardar el registro en la base de datos.
        # persona_cuenta.save()

    def agregar_entrenador(self, request):
        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas') # Obtiene lista de checkboxes activados
        usuario = request.POST['nombre_usuario']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']

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

        usuario = User(
            username = usuario,
            email = correo,
            password = make_password(password = contrasena)
        )

        usuario.save()
        usuario.groups.add(Group.objects.get(name = 'Entrenador'))

        persona_cuenta = Persona_Cuenta(
            persona_fk = persona,
            usuario_fk = usuario
        )

        persona_cuenta.save()

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