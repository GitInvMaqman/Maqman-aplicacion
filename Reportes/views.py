from django.shortcuts import render
from django.http import HttpResponse

from django.urls                import reverse_lazy
from django.views.generic       import TemplateView, ListView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models    import *
from .forms     import *
from .functions import *
from .excel     import *

import time

# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = "principal/home.html"

    def boton_prueba():
        usuarios = ModificacionesTablas.crear_datos_prueba()
        print("----------------------------------------")
        print("Usuarios creados!!")
        print("----------------------------------------")
        return usuarios

class LoginFormView(FormView):
    template_name = "principal/login.html"
    form_class    = LoginForm
    success_url   = reverse_lazy("reportesMaqman:home")

    def form_valid(self, form):
        nomUsuario = form.cleaned_data['nombre_usuario']
        contraseña = form.cleaned_data['contraseña_usuario']
        usuario    = Usuario.objects.usuario_exists(nomUsuario, contraseña)
        return Login.login_autenticacion(self, usuario, nomUsuario, contraseña)
    
class LogoutView(View):
    def get(self, request):
        return Login.cerrar_sesion(self, request)

class PerfilTemplateView(TemplateView):
    template_name = "vistas/perfil.html"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

class OperadorTemplateView(TemplateView):
    template_name = "vistas/operador.html"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context
    

class AsistenteTemplateView(TemplateView):
    template_name = "vistas/asistente.html"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

class GenReportFormView(FormView):
    model         = Reporte
    form_class    = ReporteForm
    template_name = "vistas/genReport.html"
    success_url   = reverse_lazy("reportesMaqman:genReport")

    # Validación del formulario y posterior creación de tarea.
    def form_valid(self, form):
        idPersona   = self.request.POST.get('p_id_persona')
        datos       = form.cleaned_data
        lista = self.request.POST.getlist('accesorios')

        reporteCreado = ModificacionesTablas.crear_reporte(datos, idPersona)
        if lista:
            ModificacionesTablas.crear_detalle(lista, reporteCreado)

        return super(GenReportFormView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        print(form.errors)
        self.request.session['acusete'] = 'form inválido'
        return super(GenReportFormView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        context["accesorios"] = Accesorio.objects.all()
        context["operadores"] = Usuario.objects.filter(r_id_rol = 1)
        return context

class VerReportListView(ListView):
    model               = Reporte
    paginate_by         = 9
    template_name       = "vistas/verReport.html"
    context_object_name = "reportes"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

class DetReportDetailView(DetailView):
    model               = Reporte
    template_name       = "vistas/detReport.html"
    context_object_name = "reporte"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        idReporte = self.object.id_reporte
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        context["accesorios"] = Accesorio.objects.all()
        detalle = AccesorioReporte.objects.filter(r_id_reporte = idReporte).values_list()
        context['detalles'] = []
        for d in detalle:
            context['detalles'].append(Accesorio.objects.get(id_accesorio = d[1]))
        return context
    

class excelReportesTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
       return ReportesExcel.reportes_persona(self, request, *args, **kwargs)

class DescargarExcelTemplateView(TemplateView):
    template_name = "vistas/descargarExcel.html"

    def reportes_totales(self):
        return ReportesExcel.reportes(self)
    def reportes_mes(self):
        return ReportesExcel.reportes_mes(self)
    def reportes_persona(self):
        return ReportesExcel.reportes_persona(self)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context