from django import forms
from django_countries.fields import CountryField

from .models import Paciente, Medicamento

import datetime

class PacienteCreateForm(forms.ModelForm):

    anio = datetime.datetime.now().year
    BIRTH_YEAR_CHOICES = (
        [i for i in reversed(range(1900,anio))]
    )
    fecnac = forms.DateField(widget = forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    fecnac.label = "Fecha de Nacimiento"
    class Meta:
        model = Paciente
        fields = [
            'nombre',
            'apellido',
            'fecnac',
            'dni',
            'mail',
            'pais',
            'medico',
        ]
        labels = {
            "nombre" : "Nombre",
            "apellido" : "Apellido",
            "dni" : "DNI",
            "mail" : "E-Mail",
            "pais" : "País",
            "medico" : "Médico",
        }


class MedicamentoCreateForm(forms.ModelForm):
    posologia_cantidad = forms.IntegerField()
    posologia_unidad = forms.CharField()

    class Meta:
        model = Medicamento
        fields = [
            'medicamento',
            'fecha_inicio',
            'fecha_fin',
        ]
