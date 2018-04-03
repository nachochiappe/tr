from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group
from django_countries.fields import CountryField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse

from medicos.models import Medico

# Create your models here.

User = settings.AUTH_USER_MODEL

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecnac = models.DateField()
    documento = models.PositiveIntegerField(unique=True, primary_key=True)
    pais = CountryField()
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        null=True,
    )
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        nombre_completo = self.usuario.last_name + ", " + self.usuario.first_name
        return nombre_completo

    def get_absolute_url(self):
        return reverse('paciente_detalle', kwargs={'id': self.documento})

class Medicamento(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
    )
    medicamento = models.CharField(max_length=50)
    posologia = models.PositiveIntegerField()
    medico = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dosis_a_tomar = models.PositiveIntegerField()
    dosis_completadas = models.PositiveIntegerField()

    def __str__(self):
        return(str(self.paciente.dni) + "_" + self.medicamento)


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
    fecha_completado = models.DateField(null=True, blank=True)

    def __str__(self):
        return(str(self.paciente.dni) + "_" + self.estudio)


@receiver(pre_save, sender=Paciente)
def pre_save(sender, instance, *args, **kwargs):
    instance.usuario.first_name = instance.usuario.first_name.capitalize()
    instance.usuario.last_name= instance.usuario.last_name.capitalize()
