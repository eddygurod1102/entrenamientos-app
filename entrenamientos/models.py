from django.db import models

class Persona(models.Model):
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
    persona_fk = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')

    def __str__(self):
        return f'{self.persona_fk.nombre} {self.persona_fk.apellido}'

class Entrenador(models.Model):
    persona_fk = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')

    def __str__(self):
        return f'{self.persona_fk.nombre} {self.persona_fk.apellido}'

class Disciplina(models.Model):
    nombre = models.CharField('Nombre', max_length=30)
    descripcion = models.TextField('Descripción', max_length=255, blank=True)

    def __str__(self):
        return f'{self.nombre}'

class Ejercicio(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    descripcion = models.TextField('Descripción', max_length=255, blank=True)

    def __str__(self):
        return f'{self.nombre}'

class Microciclo(models.Model):
    numero_microciclo = models.PositiveSmallIntegerField('Número de microciclo')
    atleta_fk = models.ForeignKey(Atleta, on_delete=models.CASCADE, verbose_name='Atleta')

    def get_persona(self):
        return self.atleta_fk.persona_fk

    def __str__(self):
        return f'Microciclo {self.numero_microciclo} - {self.get_persona().nombre} {self.get_persona().apellido}'

class Dia_Entrenamiento(models.Model):
    titulo = models.CharField('Título', max_length=255)
    microciclo_fk = models.ForeignKey(Microciclo, on_delete=models.CASCADE, verbose_name='Microciclo')

    # Obtener el nombre completo del atleta
    def get_microciclo_atleta(self):
        return f'{self.microciclo_fk.atleta_fk.persona_fk.nombre} {self.microciclo_fk.atleta_fk.persona_fk.apellido}'

    # Obtener el número del microciclo
    def get_microciclo_numero(self):
        return self.microciclo_fk.numero_microciclo

    def __str__(self):
        return f'{self.titulo} - Microciclo {self.get_microciclo_numero()} - {self.get_microciclo_atleta()}'

class Atletas_Disciplina(models.Model):
    atleta_fk = models.ManyToManyField(Atleta, verbose_name='Atleta')
    disciplina_fk = models.ManyToManyField(Disciplina, verbose_name='Disciplina')

    def get_nombre_atleta(self):
        return self.atleta_fk.first().persona_fk.nombre
    
    def get_apellido_atleta(self):
        return self.atleta_fk.first().persona_fk.apellido

    def get_nombre_disciplina(self):
        return self.disciplina_fk.first().nombre

    def __str__(self):
        return f'{self.get_nombre_atleta()} {self.get_apellido_atleta()} - {self.get_nombre_disciplina()}'

class Entrenadores_Disciplina(models.Model):
    entrenador_fk = models.ManyToManyField(Entrenador, verbose_name='Entrenador')
    disciplina_fk = models.ManyToManyField(Disciplina, verbose_name='Disciplina')

    def get_nombre_entrenador(self):
        return self.entrenador_fk.first().persona_fk.nombre

    def get_apellido_entrenador(self):
        return self.entrenador_fk.first().persona_fk.apellido

    def get_nombre_disciplina(self):
        return self.disciplina_fk.first().nombre

    def __str__(self):
        return f'{self.get_nombre_entrenador()} {self.get_apellido_entrenador()} - {self.get_nombre_disciplina()}'

class Dias_Ejercicios(models.Model):
    dias_entrenamiento_fk = models.ManyToManyField(Dia_Entrenamiento, verbose_name='Día de entrenamiento')
    ejercicios_fk = models.ManyToManyField(Ejercicio, verbose_name='Ejercicio')
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
        return f'{self.dias_entrenamiento_fk.first().__str__()} - {self.ejercicios_fk.first().__str__()}'

class Entrenadores_Microciclo(models.Model):
    entrenadores_fk = models.ManyToManyField(Entrenador, verbose_name='Entrenador')
    microciclo_fk = models.ManyToManyField(Microciclo, verbose_name='Microciclo')

    def __str__(self):
        return f'{self.entrenadores_fk.first().__str__()} - {self.microciclo_fk.first().__str__()}'