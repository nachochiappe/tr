from django import forms

from .models import Especialidad, Medico


class EspecialidadCreateForm(forms.ModelForm):

    class Meta:
        model = Especialidad
        fields = [
            'nombre',
        ]
        labels = {
            "especialidad" : "Especialidad"
        }


class MedicoCreateForm(forms.ModelForm):

    class Meta:
        model = Medico
        fields = [
            'nombre',
            'apellido',
            'dni',
            'mail',
            'especialidad',
        ]
        labels = {
            "nombre" : "Nombre",
            "apellido" : "Apellido",
            "dni" : "DNI",
            "mail" : "E-Mail",
            "especialidad" : "Especialidad"
        }