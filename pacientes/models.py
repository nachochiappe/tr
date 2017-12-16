from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from medicos.models import Medico

# Create your models here.

User = settings.AUTH_USER_MODEL

class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecnac = models.DateField()
    dni = models.PositiveIntegerField(unique=True)
    mail = models.EmailField()
    pais = CountryField()
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        null=True,
    )
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        nombre_completo = self.apellido + ", " + self.nombre
        return nombre_completo

    def get_absolute_url(self):
        return reverse('paciente-detalle', kwargs={'id': self.id})

class Medicamento(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
    )
    medicamento = models.CharField(max_length=50)
    posologia = models.CharField(max_length=50)
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dosis_completadas = models.PositiveIntegerField()


class Estudio(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
    )
    estudio = models.CharField(max_length=100)
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
    )
    fecha_solicitud = models.DateField()
    fecha_completado = models.DateField()
    estado = models.CharField(max_length=20)


@receiver(pre_save, sender=Paciente)
def pre_save(sender, instance, *args, **kwargs):
    instance.nombre = instance.nombre.capitalize()
    instance.apellido = instance.apellido.capitalize()