from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
                Q(usuario__last_name__iexact=slug) |
                Q(usuario__last_name__icontains=slug)
            )
        else:
            queryset = Paciente.objects.all().order_by('usuario__last_name')
        return queryset


# Detalle de Pacientes

def obtener_obj(self, *args, **kwargs):
    paciente_id = self.kwargs.get('id')
    paciente = get_object_or_404(Paciente, documento=paciente_id)
    todos_los_medicamentos = Medicamento.objects.filter(paciente=paciente)
    medicamentos_vigentes = Medicamento.objects.filter(paciente=paciente).select_related()
    medicamentos_vigentes = medicamentos_vigentes.filter(fecha_fin__gte=datetime.date.today())
    fecha_hoy = datetime.date.today()
    medicamentos_sin_tomar = []
    for medicamento in medicamentos_vigentes:
        dif_dias = (fecha_hoy - medicamento.fecha_inicio).days
        dif_dias_en_minutos = dif_dias * 24 * 60
        dosis_esperadas = dif_dias_en_minutos / medicamento.posologia
        if medicamento.dosis_completadas < dosis_esperadas:
            medicamentos_sin_tomar.append(medicamento.medicamento)
    medicamentos_en_falta = 0
    if medicamentos_sin_tomar:
        medicamentos_en_falta = 1
    medicamentos_novigentes = Medicamento.objects.filter(paciente=paciente).select_related()
    medicamentos_novigentes = medicamentos_novigentes.filter(fecha_fin__lt=datetime.date.today())
    estudios_vigentes = Estudio.objects.filter(paciente=paciente).select_related()
    estudios_vigentes = estudios_vigentes.filter(fecha_completado__isnull=True)
    estudios_novigentes = Estudio.objects.filter(paciente=paciente).select_related()
    estudios_novigentes = estudios_novigentes.filter(fecha_completado__isnull=False)
    obj = {
        'paciente': paciente,
        'medicamentos_vigentes': medicamentos_vigentes,
        'medicamentos_novigentes': medicamentos_novigentes,
        'estudios_vigentes': estudios_vigentes,
        'estudios_novigentes': estudios_novigentes,
        'medicamentos_sin_tomar': medicamentos_sin_tomar,
        'medicamentos_en_falta': medicamentos_en_falta
    }
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
    success_url = '/pacientes/'

    def form_valid(self, form):
        c = {'form': form, }
        user = form.save(commit=False)
        username = form.cleaned_data['documento']
        password = form.cleaned_data['documento']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        fecnac = form.cleaned_data['fecnac']
        pais = form.cleaned_data['pais']
        medico = form.cleaned_data['medico']
        user.username = username
        user.set_password(password)
        grupo = Group.objects.get(name='pacientes')
        user.save()
        user.groups.add(grupo)
        Paciente.objects.create(
            usuario=user,
            documento=username,
            fecnac=fecnac,
            pais=pais,
            medico=medico
        )
        return super().form_valid(form)


def tomar_medicacion(request):
    if request.method == 'POST':
        id = request.POST['id']
        medicamento = Medicamento.objects.select_related().get(id=id)
        dosis = medicamento.dosis_completadas + 1
        medicamento.dosis_completadas = dosis
        medicamento.save()
    return HttpResponse(dosis)


def borrar_medicamento(request):
    if request.method == 'POST':
        id = request.POST['id']
        Medicamento.objects.filter(id=id).select_related().delete()
    return HttpResponse()


def completar_estudio(request):
    if request.method == 'POST':
        id = request.POST['id']
        estudio = Estudio.objects.select_related().get(id=id)
        estudio.fecha_completado = datetime.date.today()
        estudio.save()
    return HttpResponse()


def borrar_estudio(request):
    if request.method == 'POST':
        id = request.POST['id']
        Estudio.objects.filter(id=id).select_related().delete()
    return HttpResponse()


def obtener_especialidades(request):
    especialidades = Especialidad.objects.all().values()
    return JsonResponse({"especialidades": list(especialidades)})


def obtener_medicos(request, id):
    medicos = Medico.objects.filter(especialidad=id).select_related().values()
    lista_medicos = []
    for medico in medicos:
        datos_medico = {}
        usuario = User.objects.get(pk=medico['usuario_id'])
        datos_medico["nombre"] = usuario.last_name + ", " + usuario.first_name
        datos_medico["documento"] = medico['documento']
        lista_medicos.append(datos_medico)
    return JsonResponse({"medicos": lista_medicos})


def derivar_paciente(request):
    if request.method == 'POST':
        id_paciente = request.POST['id_paciente']
        id_medico = request.POST['id_medico']
        paciente = Paciente.objects.filter(documento=id_paciente).select_related().update(medico=id_medico)
    return HttpResponse()

def eliminar_paciente(request):
    if request.method == 'POST':
        id_paciente = request.POST['id']
        paciente = Paciente.objects.filter(documento=id_paciente).select_related().delete()
    return HttpResponse()

def eliminar_medico(request):
    if request.method == 'POST':
        id_medico = request.POST['id']
        medico = Medico.objects.filter(documento=id_medico).select_related().delete()
    return HttpResponse()

def enviar_recordatorio(request):
    if request.method == 'POST':
        id_paciente = request.POST['id']
        paciente = Paciente.objects.filter(documento=id_paciente).select_related().get()
        subject = 'TR - Transaction Rheumatology: Recordatorio de medicamentos'
        html_message = render_to_string('mail_template.html', {'context': 'values'})
        plain_message = strip_tags(html_message)
        from_email = 'TR - Transaction Rheumatology <admin@transactionrheumatology.com.ar>'
        to = paciente.usuario.email
        send_mail(subject, plain_message, from_email, [to], html_message=html_message, fail_silently=False)
    return HttpResponse()
