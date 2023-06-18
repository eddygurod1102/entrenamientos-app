from django.db import models
from django.urls import reverse

class Persona(models.Model):
    class Meta():
        db_table = 'persona'

    nombre = models.CharField('Nombre', max_length=255)
    apellido = models.CharField('Apellido', max_length=255)
    edad = models.PositiveSmallIntegerField('Edad')

    SEXOS = [
        ('M', 'Mujer'),
        ('H', 'Hombre'),
    ]

    sexo = models.CharField('Sexo', max_length=6, choices=SEXOS)
    fotografia = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    # Retorna una lista de tuplas de entrenadores que no están registrados como atletas.
    def get_lista_entrenadores():
        personas = [] # Lista para almacenar entrenadores que no están registrados como atletas.
        atletas = []  # Lista para almacenar atletas.

        # Guardar a todos los atletas registrados en la lista atletas.
        for atleta in Atleta.objects.all():
            atletas.append(atleta.persona_fk)

        # Verificar si el entrenador no está registrado en la tabla de atletas. Si no lo
        # está, se agrega a la lista personas (lista que se usará como select para el
        # formulario).
        for entrenador in Entrenador.objects.all():
            if not atletas.count(entrenador.persona_fk):
                tupla = (entrenador.persona_fk.pk, entrenador.__str__())
                personas.append(tupla)

        return personas

    # Retorna una lista de tuplas de atletas que no están registrados como entrenadores.
    def get_lista_atletas():
        personas = []     # Lista para almacenar atletas que no están registrados como entrenadores.
        entrenadores = [] # Lista para almacenar entrenadores.
        
        # Guardar a todos los entrenadores registrados en la lista entrenadores.
        for entrenador in Entrenador.objects.all():
            entrenadores.append(entrenador.persona_fk)

        # Verificar si el atleta no está registrado en la tabla de entrenadores. Si no lo
        # Está, se agrega a la lista personas (lista que se usará como select para el 
        # formulario).
        for atleta in Atleta.objects.all():
            if not entrenadores.count(atleta.persona_fk):
                tupla = (atleta.persona_fk.pk, atleta.__str__())
                personas.append(tupla)

        return personas

class Atleta(models.Model):
    class Meta():
        db_table = 'atleta'

    persona_fk = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')

    def get_nombre(self):
        return self.persona_fk.nombre

    def get_apellido(self):
        return self.persona_fk.apellido

    def get_edad(self):
        return self.persona_fk.edad

    def get_sexo(self):
        return self.persona_fk.sexo

    def get_nombre_completo(self):
        return f'{self.get_nombre()} {self.get_apellido()}'

    def __str__(self):
        return f'{self.persona_fk.nombre} {self.persona_fk.apellido}'

class Entrenador(models.Model):
    class Meta():
        db_table = 'entrenador'

    persona_fk = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')

    def __str__(self):
        return f'{self.persona_fk.nombre} {self.persona_fk.apellido}'

    def get_nombre(self):
        return self.persona_fk.nombre

    def get_apellido(self):
        return self.persona_fk.apellido

    def get_edad(self):
        return self.persona_fk.edad

    def get_sexo(self):
        return self.persona_fk.sexo

    # Retorna una lista de tuplas con todos los entrenadores registrados.
    # Esta función será útil para poner los entrenadores en el formulario.
    def get_queryset_tupla_entrenadores():
        lista_entrenadores = []
        contador = 1

        for e in Entrenador.objects.all():
            tupla = (contador, f'{e.get_nombre()} {e.get_apellido()}')
            lista_entrenadores.append(tupla)
            contador += 1

        return lista_entrenadores

    # Retorna una lista con todos los entrenadores registrados.
    def get_queryset_entrenadores():
        lista_entrenadores = []

        for e in Entrenador.objects.all():
            lista_entrenadores.append(e)

        return lista_entrenadores

class Disciplina(models.Model):
    class Meta():
        db_table = 'disciplina'

    nombre = models.CharField('Nombre', max_length=30)
    descripcion = models.TextField('Descripción', max_length=255, blank=True)

    # Retorna una lista con todas las disciplinas registradas
    def get_queryset_disciplinas():
        lista_disciplinas = []
        for d in Disciplina.objects.all():
            lista_disciplinas.append(d)

        return lista_disciplinas

    # Retorna una lista de tuplas con todas las disciplinas registradas.
    # Esta función será útil para poner las disciplinas en los formularios.
    def get_queryset_tupla_disciplinas():
        lista_disciplinas = []
        contador = 1

        for d in Disciplina.objects.all():
            tupla = (contador, d.nombre)
            lista_disciplinas.append(tupla)
            contador += 1

        return lista_disciplinas

    def __str__(self):
        return f'{self.nombre}'

class Ejercicio(models.Model):
    class Meta():
        db_table = 'ejercicio'

    nombre = models.CharField('Nombre', max_length=50)
    descripcion = models.TextField('Descripción', max_length=255, blank=True)

    def __str__(self):
        return f'{self.nombre}'

class Microciclo(models.Model):
    class Meta():
        db_table = 'microciclo'

    titulo = models.CharField('Título', max_length=255)
    numero_microciclo = models.PositiveSmallIntegerField('Número de microciclo')
    atleta_fk = models.ForeignKey(Atleta, on_delete=models.CASCADE, verbose_name='Atleta')

    def get_persona(self):
        return self.atleta_fk.persona_fk

    def get_nombre_completo_atleta(self):
        return self.atleta_fk.get_nombre_completo()

    def __str__(self):
        return f'{self.titulo} - {self.atleta_fk.__str__()}'

    # Definición de una ruta de éxito después de modificar los datos de
    # un microciclo en específico (para no declarar un 'success_url' dentro
    # de la vista).
    def get_absolute_url(self):
        return reverse(
            'microciclos_atleta',
            kwargs = {
                'pk': self.atleta_fk.pk,
            }
        )

class Dia_Entrenamiento(models.Model):
    class Meta():
        db_table = 'dia_entrenamiento'

    titulo = models.CharField('Título', max_length=255)
    microciclo_fk = models.ForeignKey(
        Microciclo,
        on_delete=models.CASCADE,
        verbose_name='Microciclo'
    )

    # Obtener el nombre completo del atleta
    def get_microciclo_atleta(self):
        return f'{self.microciclo_fk.atleta_fk.persona_fk.nombre} {self.microciclo_fk.atleta_fk.persona_fk.apellido}'

    # Obtener el número del microciclo
    def get_microciclo_numero(self):
        return self.microciclo_fk.numero_microciclo

    def __str__(self):
        return f'{self.titulo} - Microciclo {self.get_microciclo_numero()} - {self.get_microciclo_atleta()}'
    
    # Definición de ruta de éxito después de modificar los datos de
    # un día de entrenamiento en específico (para no declarar un 'success_url'
    # dentro de la vista).
    def get_absolute_url(self):
        return reverse(
            'dias_entrenamiento',
            kwargs = {
                'pk1': self.microciclo_fk.atleta_fk.pk,
                'pk2': self.pk,
            }
        )

class Atletas_Disciplina(models.Model):
    class Meta():
        db_table = 'atletas_disciplina'

    atleta_fk = models.ForeignKey(
        Atleta,
        on_delete = models.CASCADE,
        verbose_name = 'Atleta'
    )

    disciplina_fk = models.ForeignKey(
        Disciplina,
        on_delete = models.CASCADE,
        verbose_name = 'Disciplina'
    )

    def get_nombre_atleta(self):
        return self.atleta_fk.persona_fk.nombre
    
    def get_apellido_atleta(self):
        return self.atleta_fk.persona_fk.apellido

    def get_nombre_disciplina(self):
        return self.disciplina_fk.nombre

    def __str__(self):
        return f'{self.get_nombre_atleta()} {self.get_apellido_atleta()} - {self.get_nombre_disciplina()}'

class Entrenadores_Disciplina(models.Model):
    class Meta():
        db_table = 'entrenador_disciplina'

    entrenador_fk = models.ForeignKey(
        Entrenador,
        on_delete = models.CASCADE,
        verbose_name = 'Entrenador'
    )

    disciplina_fk = models.ForeignKey(
        Disciplina,
        on_delete = models.CASCADE,
        verbose_name = 'Disciplina'
    )

    def get_nombre_entrenador(self):
        return self.entrenador_fk.persona_fk.nombre

    def get_apellido_entrenador(self):
        return self.entrenador_fk.persona_fk.apellido

    def get_nombre_disciplina(self):
        return self.disciplina_fk.nombre

    def __str__(self):
        return f'{self.get_nombre_entrenador()} {self.get_apellido_entrenador()} - {self.get_nombre_disciplina()}'

class Dias_Ejercicios(models.Model):
    class Meta():
        db_table = 'dias_entrenamiento_ejercicio'

    dias_entrenamiento_fk = models.ForeignKey(
        Dia_Entrenamiento,
        on_delete = models.CASCADE,
        verbose_name = 'Día de entrenamiento'
    )

    ejercicios_fk = models.ForeignKey(
        Ejercicio,
        on_delete = models.CASCADE,
        verbose_name = 'Ejercicio'
    )

    series = models.PositiveSmallIntegerField('Series')
    repeticiones = models.PositiveSmallIntegerField('Repeticiones')

    ESCALAS = [
        ('RPE', 'RPE'),
        ('%RM', '%RM'),
        ('RIR', 'RIR'),
    ]

    escala = models.CharField('Escala de entrenamiento', choices=ESCALAS, max_length=3)
    intensidad = models.CharField('Intensidad', max_length=10)
    peso_kg = models.DecimalField('Peso (kg)', decimal_places=2, max_digits=5)

    def __str__(self):
        return f'{self.dias_entrenamiento_fk.__str__()} - {self.ejercicios_fk.__str__()}'

    # Campo derivado de la tabla Dias_Ejercicios. Obtiene el peso en libras en función
    # al peso en kilogramos.
    def get_peso_lb(self):
        peso_lb = float(self.peso_kg) * 2.2
        return round(peso_lb, 2)

    def get_absolute_url(self):
        return reverse(
            'dias_entrenamiento',
            kwargs = {
                'pk1': self.dias_entrenamiento_fk.microciclo_fk.atleta_fk.pk,
                'pk2': self.dias_entrenamiento_fk.pk
            }
        )

class Entrenadores_Microciclo(models.Model):
    class Meta():
        db_table = 'entrenador_microciclo'

    entrenador_fk = models.ForeignKey(
        Entrenador,
        on_delete = models.CASCADE,
        verbose_name = 'Entrenador'
    )

    microciclo_fk = models.ForeignKey(
        Microciclo,
        on_delete = models.CASCADE,
        verbose_name = 'Microciclo'
    )

    def __str__(self):
        return f'{self.entrenador_fk.__str__()} - {self.microciclo_fk.__str__()}'