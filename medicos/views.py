from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import EspecialidadCreateForm, MedicoCreateForm
from .models import Especialidad, Medico

# Create your views here.


# Lista de Medicos
class MedicoListView(LoginRequiredMixin, ListView):
    template_name = 'medicos/medico_list.html'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Medico.objects.filter(
                Q(apellido__iexact=slug) |
                Q(apellido__icontains=slug)
            )
        else:
            queryset = Medico.objects.all()
        return queryset


# Detalle de Médico
class MedicoDetailView(LoginRequiredMixin, DetailView):
    queryset = Medico.objects.all()

    def get_object(self, *args, **kwargs):
        medico_id = self.kwargs.get('id')
        obj = get_object_or_404(Medico, dni=medico_id)
        return obj


# Creación de Medicos
class MedicoCreateView(LoginRequiredMixin, CreateView):
    form_class = MedicoCreateForm
    template_name = 'medicos/medico_crear.html'
    success_url = '/medicos/'

    def form_valid(self, form):
        user = User.objects.create_user(str(form.cleaned_data['dni']), form.cleaned_data['mail'], str(form.cleaned_data['dni']))
        user.first_name = form.cleaned_data['nombre']
        user.last_name = form.cleaned_data['apellido']
        grupo = Group.objects.get(name='medicos')
        user.groups.add(grupo)
        user.save()
        return super().form_valid(form)


# Lista de Especialidades
class EspecialidadListView(LoginRequiredMixin, ListView):
    template_name = 'medicos/especialidad_list.html'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Especialidad.objects.filter(
                Q(nombre__iexact=slug) |
                Q(nombre__icontains=slug)
            )
        else:
            queryset = Especialidad.objects.all()
        return queryset


# Creación de Especialidades
class EspecialidadCreateView(LoginRequiredMixin, CreateView):
    form_class = EspecialidadCreateForm
    template_name = 'medicos/especialidad_crear.html'
    success_url = '/medicos/especialidades/'