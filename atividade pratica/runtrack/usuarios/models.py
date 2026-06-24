from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    class Tipo(models.TextChoices):
        ATLETA = 'ATLETA', 'Atleta'
        TREINADOR = 'TREINADOR', 'Treinador'
        ORGANIZADOR = 'ORGANIZADOR', 'Organizador'

    tipo = models.CharField(
        max_length=12,
        choices=Tipo.choices,
        default=Tipo.ATLETA
    )

    data_nasc = models.DateField(null=True, blank=True)
    cidade = models.CharField(max_length=80, blank=True)

    def is_atleta(self):
        return self.tipo == self.Tipo.ATLETA

    def is_treinador(self):
        return self.tipo == self.Tipo.TREINADOR

    def is_organizador(self):
        return self.tipo == self.Tipo.ORGANIZADOR

    def __str__(self):
        return f'{self.username} ({self.get_tipo_display()})'