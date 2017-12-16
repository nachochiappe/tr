"""tr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView

from medicos.views import *
from pacientes.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^$', PacienteListView.as_view(), name='home'),
    url(r'^pacientes/$', PacienteListView.as_view(), name='pacientes'),
    url(r'^pacientes/crear/$', PacienteCreateView.as_view(), name='paciente-crear'),
    url(r'^pacientes/(?P<id>\w+)/$', PacienteDetailView.as_view(), name='paciente-detalle'),
    url(r'^medicos/$', MedicoListView.as_view(), name='medicos'),
    url(r'^medicos/crear/$', MedicoCreateView.as_view(), name='medico-crear'),
    url(r'^medicos/especialidades/$', EspecialidadListView.as_view(), name='especialidades'),
    url(r'^medicos/especialidades/crear/$', EspecialidadCreateView.as_view(), name='especialidad-crear'),
]
