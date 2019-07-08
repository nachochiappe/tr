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
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from medicos.views import *
from pacientes.views import *

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/signup', signup, name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^$', PacienteListView.as_view(), name='home'),
    url(r'^ajax/tomar_medicacion/$', tomar_medicacion, name='tomar_medicacion'),
    url(r'^ajax/borrar_medicamento/$', borrar_medicamento, name='borrar_medicamento'),
    url(r'^ajax/completar_estudio/$', completar_estudio, name='completar_estudio'),
    url(r'^ajax/borrar_estudio/$', borrar_estudio, name='borrar_estudio'),
    url(r'^ajax/derivar_paciente/$', derivar_paciente, name='derivar_paciente'),
    url(r'^ajax/obtener_especialidades/$', obtener_especialidades, name='obtener_especialidades'),
    url(r'^ajax/obtener_medicos/(?P<id>\w+)/$', obtener_medicos, name='obtener_medicos'),
    url(r'^pacientes/crear/$', PacienteCreateView.as_view(), name='paciente_crear'),
    url(r'^pacientes/(?P<id>\w+)/alertas/$', PacienteDetailView.as_view(), name='paciente_alertas'),
    url(r'^pacientes/(?P<id>\w+)/medicamentos/$', PacienteDetailView.as_view(), name='paciente_medicamentos'),
    url(r'^pacientes/(?P<id>\w+)/estudios/$', PacienteDetailView.as_view(), name='paciente_estudios'),
    url(r'^pacientes/(?P<id>\w+)/$', PacienteDetailView.as_view(), name='paciente_detalle'),
    url(r'^pacientes/$', PacienteListView.as_view(), name='pacientes'),
    url(r'^medicos/$', MedicoListView.as_view(), name='medicos'),
    url(r'^medicos/crear/$', MedicoCreateView.as_view(), name='medico_crear'),
    url(r'^medicos/especialidades/$', EspecialidadListView.as_view(), name='especialidades'),
    url(r'^medicos/especialidades/crear/$', EspecialidadCreateView.as_view(), name='especialidad_crear'),
    url(r'^medicos/(?P<id>\w+)/pacientes/$', MedicoPacientesListView.as_view(), name='medico_pacientes'),
    url(r'^medicos/(?P<id>\w+)/alertas/$', MedicoAlertasListView.as_view(), name='medico_alertas'),
    url(r'^medicos/(?P<id>\w+)/agenda/$', MedicoDetailView.as_view(), name='medico_agenda'),
    url(r'^medicos/(?P<id>\w+)/$', MedicoDetailView.as_view(), name='medico_detalle'),
]
