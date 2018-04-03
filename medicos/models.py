from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "especialidades"


class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    documento = models.PositiveIntegerField(unique=True, primary_key=True)
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
    )
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        nombre_completo = self.usuario.last_name + ", " + self.usuario.first_name
        return nombre_completo
