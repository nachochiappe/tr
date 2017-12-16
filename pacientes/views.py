from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PacienteCreateForm
from .models import Paciente

# Create your views here.


# Lista de Pacientes
class PacienteListView(LoginRequiredMixin, ListView):
    template_name = 'pacientes/paciente_list.html'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Paciente.objects.filter(
                Q(apellido__iexact=slug) |
                Q(apellido__icontains=slug)
            )
        else:
            queryset = Paciente.objects.all()
        return queryset


# Detalle de Pacientes
class PacienteDetailView(LoginRequiredMixin, DetailView):
    queryset = Paciente.objects.all()

    def get_object(self, *args, **kwargs):
        paciente_id = self.kwargs.get('id')
        obj = get_object_or_404(Paciente, id=paciente_id)
        return obj


# Creación de Pacientes
class PacienteCreateView(LoginRequiredMixin, CreateView):
    form_class = PacienteCreateForm
    template_name = 'pacientes/paciente_crear.html'

    def form_valid(self, form):
        user = User.objects.create_user(str(form.cleaned_data['dni']), form.cleaned_data['mail'], str(form.cleaned_data['dni']))
        user.first_name = form.cleaned_data['nombre']
        user.last_name = form.cleaned_data['apellido']
        grupo = Group.objects.get(name='pacientes')
        user.groups.add(grupo)
        user.save()
        return super().form_valid(form)