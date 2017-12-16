from django.db import models

# Create your models here.


class Administrador(models.Model):
    dni = models.PositiveIntegerField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        nombre_completo = self.apellido + ", " + self.nombre
        return nombre_completo

    class Meta:
        verbose_name_plural = "administradores"

