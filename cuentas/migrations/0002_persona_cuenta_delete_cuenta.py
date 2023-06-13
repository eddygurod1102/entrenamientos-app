# Generated by Django 4.2 on 2023-05-21 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamientos', '0007_rename_ejercicio_fk_dias_ejercicios_ejercicios_fk_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona_Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='entrenamientos.persona', verbose_name='Persona')),
                ('usuario_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.DeleteModel(
            name='Cuenta',
        ),
    ]
