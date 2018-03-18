from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse

import datetime

from .forms import PacienteCreateForm, MedicamentoCreateForm, EstudioCreateForm
from .models import Paciente, Medicamento, Estudio
from medicos.models import Medico, Especialidad

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

def obtener_obj(self, *args, **kwargs):
    paciente_id = self.kwargs.get('id')
    paciente = get_object_or_404(Paciente, id=paciente_id)
    medicamentos_vigentes = Medicamento.objects.filter(paciente=paciente).values()
    medicamentos_vigentes = medicamentos_vigentes.filter(fecha_fin__gte=datetime.date.today())
    fecha_hoy = datetime.date.today()
    medicamentos_sin_tomar = []
    for medicamento in medicamentos_vigentes:
        dif_dias = fecha_hoy - medicamento['fecha_inicio']
        dif_dias_en_minutos = dif_dias.days * 24 * 60
        dosis_a_tomar = dif_dias_en_minutos / medicamento['posologia']
        print(medicamento['medicamento'])
        print(dosis_a_tomar)
        print(medicamento['dosis_completadas'])
        if medicamento['dosis_completadas'] < dosis_a_tomar:
            medicamentos_sin_tomar.append(medicamento['medicamento'])
    print(medicamentos_sin_tomar)
    medicamentos_novigentes = Medicamento.objects.filter(paciente=paciente).values()
    medicamentos_novigentes = medicamentos_novigentes.filter(fecha_fin__lt=datetime.date.today())
    estudios_vigentes = Estudio.objects.filter(paciente=paciente).values()
    estudios_vigentes = estudios_vigentes.filter(fecha_completado__isnull=True)
    estudios_novigentes = Estudio.objects.filter(paciente=paciente).values()
    estudios_novigentes = estudios_novigentes.filter(fecha_completado__isnull=False)
    obj = {'paciente': paciente, 'medicamentos_vigentes': medicamentos_vigentes, 'medicamentos_novigentes': medicamentos_novigentes,
    'estudios_vigentes': estudios_vigentes, 'estudios_novigentes': estudios_novigentes, 'medicamentos_sin_tomar': medicamentos_sin_tomar}
    return obj


class PacienteDisplay(DetailView):
    template_name = 'pacientes/paciente_detail.html'

    queryset = Paciente.objects.all()

    def get_object(self, *args, **kwargs):
        return obtener_obj(self, *args, **kwargs)


class PacienteMedicamentoEstudio(SingleObjectMixin, FormView):
    form_class = MedicamentoCreateForm
    template_name = 'pacientes/paciente_detail.html'

    def get_object(self, *args, **kwargs):
        return obtener_obj(self, *args, **kwargs)

    def form_valid(self, form):
        if 'medicamento' in form.cleaned_data:
            medicamento = Medicamento()
            medicamento.paciente = self.object['paciente']
            medicamento.medicamento = form.cleaned_data['medicamento']
            if form.cleaned_data['posologia_unidad'] == "horas":
                medicamento.posologia = form.cleaned_data['posologia_cantidad'] * 60
            elif form.cleaned_data['posologia_unidad'] == "dias":
                medicamento.posologia = form.cleaned_data['posologia_cantidad'] * 60 * 24
            elif form.cleaned_data['posologia_unidad'] == "semanas":
                medicamento.posologia = form.cleaned_data['posologia_cantidad'] * 60 * 24 * 7
            else:
                medicamento.posologia = form.cleaned_data['posologia_cantidad'] * 60 * 24 * 30
            medicamento.medico = medicamento.paciente.medico
            medicamento.fecha_inicio = form.cleaned_data['fecha_inicio']
            medicamento.fecha_fin = form.cleaned_data['fecha_fin']
            dif_dias = (medicamento.fecha_fin - medicamento.fecha_inicio)
            dif_dias_en_minutos = dif_dias.days * 24 * 60
            dosis_a_tomar = dif_dias_en_minutos / medicamento.posologia
            medicamento.dosis_a_tomar = dosis_a_tomar
            medicamento.dosis_completadas = 0
            medicamento.save()
            return self.render_to_response(self.get_context_data(form=form))
        elif 'estudio' in form.cleaned_data:
            estudio = Estudio()
            estudio.paciente = self.object['paciente']
            estudio.estudio = form.cleaned_data['estudio']
            estudio.medico = estudio.paciente.medico
            estudio.fecha_solicitud = datetime.date.today()
            estudio.save()
            return self.render_to_response(self.get_context_data(form=form))

        # return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'guardarmed' in request.POST:
            medform = MedicamentoCreateForm(request.POST)
            if medform.is_valid():
                return self.form_valid(medform)
            else:
                return self.form_invalid(medform)
        elif 'guardarest' in request.POST:
            estform = EstudioCreateForm(request.POST)
            if estform.is_valid():
                return self.form_valid(estform)
            else:
                return self.form_invalid(estform)
        else:
            print("error")
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


def tomar_medicacion(request):
    if request.method == 'POST':
        id = request.POST['id']
        medicamento = Medicamento.objects.get(id=id)
        dosis = medicamento.dosis_completadas + 1
        medicamento.dosis_completadas = dosis
        medicamento.save()
    return HttpResponse(dosis)


def borrar_medicamento(request):
    if request.method == 'POST':
        id = request.POST['id']
        Medicamento.objects.filter(id=id).delete()
    return HttpResponse()


def borrar_estudio(request):
    if request.method == 'POST':
        id = request.POST['id']
        Estudio.objects.filter(id=id).delete()
    return HttpResponse()


def obtener_especialidades(request):
    especialidades = Especialidad.objects.all().values()
    return JsonResponse({"especialidades": list(especialidades)})


def obtener_medicos(request, id):
    medicos = Medico.objects.filter(especialidad=id).values()
    return JsonResponse({"medicos": list(medicos)})


def derivar_paciente(request):
    if request.method == 'POST':
        id_paciente = request.POST['id_paciente']
        id_medico = request.POST['id_medico']
        paciente = Paciente.objects.filter(id=id_paciente).update(medico=id_medico)
    return HttpResponse()