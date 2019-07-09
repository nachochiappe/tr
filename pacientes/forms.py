from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, MultiWidgetField
from django_countries.fields import LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from django_countries import countries
from django.contrib.auth.models import User
from .models import Paciente, Medicamento, Estudio
from medicos.models import Medico

import datetime

class PacienteCreateForm(forms.ModelForm):

    anio = datetime.datetime.now().year + 1
    BIRTH_YEAR_CHOICES = (
        [i for i in reversed(range(1900,anio))]
    )
    fecnac = forms.DateField(widget = forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    # fecnac.layout = Layout(
    #     MultiWidgetField('days', attrs=({'style': 'width: 33%; display: inline-block;'})),
    #     MultiWidgetField('months', attrs=({'style': 'width: 33%; display: inline-block;'})),
    #     MultiWidgetField('years', attrs=({'style': 'width: 33%; display: inline-block;'})))
    fecnac.label = "Fecha de Nacimiento"
    documento = forms.IntegerField()
    pais = LazyTypedChoiceField(choices=countries)
    medico = forms.ModelChoiceField(queryset=Medico.objects.all())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'documento', 'fecnac', 'pais', 'medico']
        widgets = {'pais': CountrySelectWidget()}
        labels = {
            "first_name" : "Nombre",
            "last_name" : "Apellido",
            "documento" : "Documento",
            "email" : "Email",
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

class EstudioCreateForm(forms.ModelForm):

    class Meta:
        model = Estudio
        fields = [
            'estudio',
        ]
