# Generated by Django 4.2 on 2023-05-05 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamientos', '0003_alter_dias_ejercicios_escala_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dias_ejercicios',
            name='dias_entrenamiento_fk',
        ),
        migrations.RemoveField(
            model_name='dias_ejercicios',
            name='ejercicios_fk',
        ),
        migrations.RemoveField(
            model_name='entrenadores_disciplina',
            name='disciplina_fk',
        ),
        migrations.RemoveField(
            model_name='entrenadores_disciplina',
            name='entrenador_fk',
        ),
        migrations.RemoveField(
            model_name='entrenadores_microciclo',
            name='entrenadores_fk',
        ),
        migrations.RemoveField(
            model_name='entrenadores_microciclo',
            name='microciclo_fk',
        ),
        migrations.DeleteModel(
            name='Atletas_Disciplina',
        ),
        migrations.DeleteModel(
            name='Dias_Ejercicios',
        ),
        migrations.DeleteModel(
            name='Entrenadores_Disciplina',
        ),
        migrations.DeleteModel(
            name='Entrenadores_Microciclo',
        ),
    ]