from django.db import models

# Create your models here.


class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "especialidades"


class Medico(models.Model):
    dni = models.PositiveIntegerField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
    )
    mail = models.EmailField()
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        nombre_completo = self.apellido + ", " + self.nombre
        return nombre_completo
