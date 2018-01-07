from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PacienteCreateForm, MedicamentoCreateForm
from .models import Paciente, Medicamento, Estudio

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
class PacienteDisplay(DetailView):
    template_name = 'pacientes/paciente_detail.html'

    queryset = Paciente.objects.all()

    def get_object(self, *args, **kwargs):
        paciente_id = self.kwargs.get('id')
        paciente = get_object_or_404(Paciente, id=paciente_id)
        medicamentos = Medicamento.objects.filter(paciente=paciente).values()
        obj = {'paciente': paciente, 'medicamentos': medicamentos}
        return obj


class PacienteMedicamentoEstudio(SingleObjectMixin, FormView):
    form_class = MedicamentoCreateForm
    template_name = 'pacientes/paciente_detail.html'

    def get_object(self, *args, **kwargs):
        paciente_id = self.kwargs.get('id')
        paciente = get_object_or_404(Paciente, id=paciente_id)
        medicamentos = Medicamento.objects.filter(paciente=paciente).values()
        obj = {'paciente': paciente, 'medicamentos': medicamentos}
        return obj

    def form_valid(self, form):
        medicamento = Medicamento()
        medicamento.paciente = self.object['paciente']
        medicamento.medicamento = form.cleaned_data['medicamento']
        medicamento.posologia = form.cleaned_data['posologia']
        medicamento.medico = medicamento.paciente.medico
        medicamento.fecha_inicio = form.cleaned_data['fecha_inicio']
        medicamento.fecha_fin = form.cleaned_data['fecha_fin']
        medicamento.dosis_completadas = 0
        medicamento.save()
        return self.render_to_response(self.get_context_data(form=form))
        # return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MedicamentoCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return self.form_valid(form)
        else:
            print("not valid")
            print(form.cleaned_data)
            return self.form_invalid(form)
        # return super().post(request, *args, **kwargs)


class PacienteDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = PacienteDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PacienteMedicamentoEstudio.as_view()
        return view(request, *args, **kwargs)


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
