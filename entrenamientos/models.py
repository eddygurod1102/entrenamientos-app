from django.db import models

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

    numero_microciclo = models.PositiveSmallIntegerField('Número de microciclo')
    atleta_fk = models.ForeignKey(Atleta, on_delete=models.CASCADE, verbose_name='Atleta')

    def get_persona(self):
        return self.atleta_fk.persona_fk

    def __str__(self):
        return f'Microciclo {self.numero_microciclo} - {self.get_persona().nombre} {self.get_persona().apellido}'

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

    ejercicio_fk = models.ForeignKey(
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