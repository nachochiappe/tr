from django import forms
from django_countries.fields import CountryField

from .models import Paciente

class PacienteCreateForm(forms.ModelForm):

    fecnac = forms.DateField(widget = forms.SelectDateWidget)
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
        ]
        labels = {
            "nombre" : "Nombre",
            "apellido" : "Apellido",
            "dni" : "DNI",
            "mail" : "E-Mail",
            "pais" : "País",
        }