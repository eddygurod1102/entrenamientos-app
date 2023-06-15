from django.db import models
from django.contrib.auth.models import User
from entrenamientos.models import Persona

class Persona_Cuenta(models.Model):
    persona_fk = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name='Persona')
    usuario_fk = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')

    def get_id_atleta(self):
        return self.persona_fk.atleta_set.first().pk