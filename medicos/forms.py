from django import forms
from django.contrib.auth.models import User
from .models import Especialidad, Medico


class EspecialidadCreateForm(forms.ModelForm):

    class Meta:
        model = Especialidad
        fields = ['nombre']
        labels = {
            "especialidad" : "Especialidad"
        }


class UserMedicoCreateForm(forms.ModelForm):

    documento = forms.IntegerField()
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'documento', 'especialidad']
        labels = {
            "first_name" : "Nombre",
            "last_name" : "Apellido",
            "email" : "Email",
            "documento" : "Documento",
            "especialidad" : "Especialidad",
        }