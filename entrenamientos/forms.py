from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from .models import *
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

    # Pone como checkboxes las disciplinas disponibles.
    def set_disciplinas(self, disciplinas):
        self.fields['disciplinas'].widget.choices=disciplinas

    # Cambia el texto del label de las disciplinas dependiendo si se agregará un
    # atleta o un entrenador.
    def es_entrenador_atleta(self, bandera):
        if bandera == 'Entrenador':
            self.fields['disciplinas'].label = 'Disciplina(s) que imparte'
        else:
            self.fields['disciplinas'].label = 'Disciplina(s) que practica'
        return self    

    # Agrega a un atleta a la base de datos (método utilizado en form_valid).
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

        # Creación de un nuevo objeto Persona.
        persona = Persona(
            nombre = nombre,
            apellido = apellido,
            edad = edad,
            sexo = sexo,
            fotografia = fotografia
        )

        # Guardar el registro de la persona en la base de datos.
        persona.save()

        # Creación de un objeto Atleta, el cuál, obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Atletas.
        atleta = Atleta(persona_fk = persona)
        # atleta.persona_fk = persona
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

        # Creación de un uevo objeto User.
        usuario = User(
            username = usuario,
            email = correo,
            password = make_password(contrasena)
        )


        # Guardar el registro del usuario en la base de datos.
        usuario.save()

        # Agregamos al usuario en el grupo de atletas.
        usuario.groups.add(Group.objects.get(name = 'Atleta'))

        # Creación de un nuevo objecto Persona_Cuenta. Recuerda: una persona sólo puede tener
        # una cuenta.
        persona_cuenta = Persona_Cuenta(
            persona_fk = persona,
            usuario_fk = usuario
        )

        # Guardar el registro en la base de datos.
        persona_cuenta.save()

    # Agrega un entrenador en la base de datos (método utilizado en form_valid).
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

        # Creación de un nuevo objeto User.
        usuario = User(
            username = usuario,
            email = correo,
            password = make_password(password = contrasena)
        )

        # Guardar el registro de lusuario en la base de datos.
        usuario.save()

        # Agregamos al usuario en el grupo de entrenadores.
        usuario.groups.add(Group.objects.get(name = 'Entrenador'))

        # Creación de un nuevo objeto Persona_Cuenta. Recuerda: una persona sólo puede tener
        # sola cuenta.
        persona_cuenta = Persona_Cuenta(
            persona_fk = persona,
            usuario_fk = usuario
        )

        # Guardar el registro en la base de datos.
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

    def agregar_atleta(self, request):
        # Obtener los datos del formulario.
        persona_id = request.POST['personas']
        disciplinas = request.POST.getlist('disciplinas')

        # Obtener a la persona mediante su llave primaria.
        persona = Persona.objects.get(pk=persona_id)

        # Creación de un objeto Atleta, el cuál obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Atleta.
        atleta = Atleta(persona_fk=persona)
        atleta.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Por cada checkbox de disciplinas seleccionado, se agrega un registro en la tabla
        # Atletas_Disciplina, con la información del atleta y de la disciplina.
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
        persona_id = request.POST['personas']
        disciplinas = request.POST.getlist('disciplinas')

        # Obtener a la persona mediante su llave primaria.
        persona = Persona.objects.get(pk=persona_id)

        # Creación de un objeto Entrenador, el cuál obtiene los datos del objeto persona, para luego
        # después, guardarlo en la base de datos, pero ahora en la tabla Entrenadores.
        entrenador = Entrenador(persona_fk=persona)
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

# Formulario para editar la información de una persona.
class FormularioEditarPersona(forms.Form):
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
    # Funciones que se mandan a llamar para editar la información de la persona
    def set_nombre(self, nombre):
        self.fields['nombre'].widget.attrs['value'] = nombre

    def set_apellido(self, apellido):
        self.fields['apellido'].widget.attrs['value'] = apellido

    def set_edad(self, edad):
        self.fields['edad'].widget.attrs['value'] = edad

    def set_sexo(self, sexo):
        self.fields['sexo'].widget.attrs['selected'] = sexo

    def set_disciplinas(self, disciplinas):
        self.fields['disciplinas'].widget.choices = disciplinas

    def editar_atleta(self, request, pk):
        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=pk)

        # Obtener a la persona en base a la información del atleta.
        persona = Persona.objects.get(pk=atleta.persona_fk.pk)

        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas')

        # Actualizar los datos de la persona.
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Actualizar el registro.
        persona.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Recorrido de la lista de checkboxes. Verifica cúales están seleccionados, y cuáles
        # no. Para todo checkbox seleccionado, se busca en la tabla Atletas_Disciplina si existe
        # un registro con la información del atleta y la disciplina. Si no existe, entonces, se crea
        # un nuevo registro en la tabla Atletas_Disciplina, caso contrario, si ya existe, omite el paso
        # anterior. Para todo checkbox no seleccionado, se busca en la tabla Atletas_Disciplina si existe
        # un registro con la información del atleta y la disciplina. Si existe, entonces, se elimina el
        # registro en la tabla Atletas_Disciplina, caso contrario, si no existe, omite el paso anterior.
        # Todo lo anterior se puede interpretar como: ¿Cuáles son las nuevas disciplinas que el atleta
        # entrena, y cuáles ha dejado de entrenar?
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                try:
                    atleta.atletas_disciplina_set.get(disciplina_fk=disciplina)
                except Atletas_Disciplina.DoesNotExist:
                    atleta.atletas_disciplina_set.create(atleta_fk=atleta, disciplina_fk=disciplina)
                else:
                    pass
                contador += 1
            else:
                try:
                    atleta.atletas_disciplina_set.get(disciplina_fk=disciplina)
                except Atletas_Disciplina.DoesNotExist:
                    pass
                else:
                    Atletas_Disciplina.objects.get(atleta_fk=atleta, disciplina_fk=disciplina).delete()
                contador += 1
    
    def editar_entrenador(self, request, pk):
        # Obtener al entrenador mediante su llave primaria.
        entrenador = Entrenador.objects.get(pk=pk)

        # Obtener a la persona en base a la información del entrenador.
        persona = Persona.objects.get(pk=entrenador.persona_fk.pk)

        # Obtener los datos del formulario.
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        sexo = request.POST['sexo']
        fotografia = request.POST['fotografia']
        disciplinas = request.POST.getlist('disciplinas')

        # ACtualiza los datos de la persona.
        persona.nombre = nombre
        persona.apellido = apellido
        persona.edad = edad
        persona.sexo = sexo
        persona.fotografia = fotografia

        # Actualizar el registro.
        persona.save()

        contador = 1 # Variable para recorrer la lista de checkboxes de las disciplinas.

        # Recorrido de la lista de checkboxes. Verifica cuáles están seleccionados, y cuáles
        # no. Para todo checkbox seleccionado, se busca en la tabla Entrenadores_Disciplina si existe
        # un registro con la información del entrenador y la disciplina. Si no existe, entonces, se crea
        # un nuevo registro en la tabla Entrenadores_Disciplina, caso contrario, si ya existe,omite el paso
        # anterior. Para todo checkbox no seleccionado, se busca en la tabla Entrenadores_Disciplina si existe
        # un registro con la información del entrenador y la disciplina. Si existe, entonces, se elimina el
        # registro en la tabla Entrenadores_Disciplina, caso contrario, si no existem omite el paso anterior.
        # Todo lo anterior se puede interpretar como: ¿Cuáles son las nuevas disciplinas que el entrenador
        # imparte, y cuáles ha dejado de impartir?
        for disciplina in Disciplina.get_queryset_disciplinas():
            if disciplinas.count(f'{contador}') == 1:
                try:
                    entrenador.entrenadores_disciplina_set.get(disciplina_fk=disciplina)
                except Entrenadores_Disciplina.DoesNotExist:
                    entrenador.entrenadores_disciplina_set.create(entrenador_fk=entrenador, disciplina_fk=disciplina)
                else:
                    pass
                contador += 1
            else:
                try:
                    entrenador.entrenadores_disciplina_set.get(disciplina_fk=disciplina)
                except Entrenadores_Disciplina.DoesNotExist:
                    pass
                else:
                    Entrenadores_Disciplina.objects.get(entrenador_fk=entrenador, disciplina_fk=disciplina).delete()
                contador += 1

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

    def agregar_microciclo(self, request, pk):
        # Obtener datos del formulario.
        titulo = request.POST['titulo']
        entrenadores = request.POST.getlist('entrenadores')

        # Obtener al atleta mediante su llave primaria.
        atleta = Atleta.objects.get(pk=pk)

        # Creación de un nuevo objeto Microciclo.
        microciclo = Microciclo()
        microciclo.titulo = titulo

        # Para registrar el número del microciclo del atleta, tomamos todos los que tiene registrados,
        # y le sumamos 1 al resultado.
        microciclo.numero_microciclo = Microciclo.objects.filter(atleta_fk=atleta).count() + 1
        microciclo.atleta_fk = atleta

        # Guardar microciclo en la base de datos.
        microciclo.save()

        contador = 1 # Variable para recorres la lista de checkboxes de los entrenadores.

        # Por cada checkbox de entrenadores seleccionado, se agrega un registro en la tabla
        # Entrenadores_Microciclo, con la información del entrenador y del microciclo.
        for entrenador in Entrenador.get_queryset_entrenadores():
            if entrenadores.count(f'{contador}') == 1:
                entrenador_microciclo = Entrenadores_Microciclo(
                    entrenador_fk = entrenador,
                    microciclo_fk = microciclo
                )

                entrenador_microciclo.save()
                contador += 1
            else:
                contador += 1    

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

    def agregar_dia(self, request, pk1, pk2):
        # Obtener datos del formulario.
        titulo = request.POST['titulo']

        # Obtener el microciclo mediante su llave primaria.
        microciclo = Microciclo.objects.get(pk=pk2)

        # Creación de un objeto Dia_Entrenamiento
        dia_entrenamiento = Dia_Entrenamiento()
        dia_entrenamiento.titulo = titulo
        dia_entrenamiento.microciclo_fk = microciclo

        # Guardarlo en la base de datos.
        dia_entrenamiento.save()  

# Formulario para agregar un ejercicio a un día de entrenamiento
class FormularioEjercicio(ModelForm):
    class Meta():
        model = Dias_Ejercicios
        fields = ['ejercicios_fk', 'series', 'repeticiones', 'escala', 'intensidad', 'peso_kg']

    def agregar_ejercicio(self, request, pk):
        dia_entrenamiento = Dia_Entrenamiento.objects.get(pk = pk)

        # Obtener los datos del formulario.
        ejercicio_pk = request.POST['ejercicios_fk']
        series = request.POST['series']
        repeticiones = request.POST['repeticiones']
        escala = request.POST['escala']
        intensidad = request.POST['intensidad']
        peso_kg = request.POST['peso_kg']

        # Obtener el ejercicio mediante la llave primaria que nos da el select.
        ejercicio = Ejercicio.objects.get(pk=ejercicio_pk)

        # Creación de un objeto Dias_Ejercicios.
        dias_ejercicios = Dias_Ejercicios()
        dias_ejercicios.dias_entrenamiento_fk = dia_entrenamiento
        dias_ejercicios.ejercicios_fk = ejercicio
        dias_ejercicios.series = series
        dias_ejercicios.repeticiones = repeticiones
        dias_ejercicios.escala = escala
        dias_ejercicios.intensidad = intensidad
        dias_ejercicios.peso_kg = peso_kg
        
        # Guardar en la base de datos.
        dias_ejercicios.save()