from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    documento = models.PositiveIntegerField(unique=True, primary_key=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        nombre_completo = self.apellido + ", " + self.nombre
        return nombre_completo

    class Meta:
        verbose_name_plural = "administradores"

