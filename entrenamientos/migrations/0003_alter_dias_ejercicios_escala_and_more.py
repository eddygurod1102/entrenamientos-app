# Generated by Django 4.2 on 2023-05-05 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamientos', '0002_dias_ejercicios_escala_dias_ejercicios_intensidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dias_ejercicios',
            name='escala',
            field=models.CharField(choices=[('RPE', 'RPE'), ('%RM', '%RM'), ('RIR', 'RIR')], max_length=3, verbose_name='Escala de entrenamiento'),
        ),
        migrations.AlterField(
            model_name='dias_ejercicios',
            name='intensidad',
            field=models.CharField(max_length=10, verbose_name='Intensidad'),
        ),
        migrations.AlterField(
            model_name='dias_ejercicios',
            name='peso_kg',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Peso (kg)'),
        ),
        migrations.AlterField(
            model_name='dias_ejercicios',
            name='repeticiones',
            field=models.PositiveSmallIntegerField(verbose_name='Repeticiones'),
        ),
        migrations.AlterField(
            model_name='dias_ejercicios',
            name='series',
            field=models.PositiveSmallIntegerField(verbose_name='Series'),
        ),
        migrations.AlterModelTable(
            name='atleta',
            table='atleta',
        ),
        migrations.AlterModelTable(
            name='atletas_disciplina',
            table='atletas_disciplina',
        ),
        migrations.AlterModelTable(
            name='dia_entrenamiento',
            table='dia_entrenamiento',
        ),
        migrations.AlterModelTable(
            name='dias_ejercicios',
            table='dias_entrenamiento_ejercicio',
        ),
        migrations.AlterModelTable(
            name='disciplina',
            table='disciplina',
        ),
        migrations.AlterModelTable(
            name='ejercicio',
            table='ejercicio',
        ),
        migrations.AlterModelTable(
            name='entrenador',
            table='entrenador',
        ),
        migrations.AlterModelTable(
            name='entrenadores_disciplina',
            table='entrenador_disciplina',
        ),
        migrations.AlterModelTable(
            name='entrenadores_microciclo',
            table='entrenador_microciclo',
        ),
        migrations.AlterModelTable(
            name='microciclo',
            table='microciclo',
        ),
        migrations.AlterModelTable(
            name='persona',
            table='persona',
        ),
    ]