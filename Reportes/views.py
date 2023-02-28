#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from django.urls                import reverse_lazy
from django.views.generic       import TemplateView, ListView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models    import *
from .forms     import *
from .functions import *
from .excel     import *

#----------------------------------------------------------------------------------------------------------------#
# Vistas
#----------------------------------------------------------------------------------------------------------------#

# ------------------------- #
# Home                      #
# ------------------------- #
class HomeTemplateView(TemplateView):
    template_name = "principal/home.html"

# ------------------------- #
# Inicio y cierre de Sesión #
# ------------------------- #

class LoginFormView(FormView):
    template_name = "principal/login.html"
    form_class    = LoginForm

    # Validación de los datos para su posterior inicio de sesión
    def form_valid(self, form):
        nomUsuario = form.cleaned_data['nombre_usuario']
        contraseña = form.cleaned_data['contraseña_usuario']
        usuario    = Usuario.objects.usuario_exists(nomUsuario, contraseña)
        return Login.login_autenticacion(self, usuario, nomUsuario, contraseña)
    
class LogoutView(View):
    def get(self, request):
        return Login.cerrar_sesion(self, request)

# ------------------------- #
# Usuario                   #
# ------------------------- #

class PerfilTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "vistas/perfil.html"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context

class PrincipalTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "vistas/vista-principal.html"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

# ------------------------- #
# Reportes                  #
# ------------------------- #

class GenReportFormView(LoginRequiredMixin, FormView):
    model         = Reporte
    form_class    = ReporteForm
    template_name = "vistas/genReport.html"
    success_url   = reverse_lazy("reportesMaqman:genReport")

    # Validación del formulario y posterior creación de tarea.
    def form_valid(self, form):
        datos     = form.cleaned_data
        idPersona = self.request.POST.get('p_id_persona')
        lista     = self.request.POST.getlist('accesorios')

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

class VerReportListView(LoginRequiredMixin, ListView):
    model               = Reporte
    paginate_by         = 9
    template_name       = "vistas/verReport.html"
    context_object_name = "reportes"

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context

class DetReportDetailView(LoginRequiredMixin, DetailView):
    model               = Reporte
    template_name       = "vistas/detReport.html"
    context_object_name = "reporte"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        idReporte             = self.object.id_reporte
        context               = super().get_context_data(**kwargs)
        context["accesorios"] = Accesorio.objects.all()
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        # Se obtienen los accesorios seleccionados en el reporte.
        detalle               = AccesorioReporte.objects.filter(r_id_reporte = idReporte).values_list()
        context['detalles']   = []
        for d in detalle:
            context['detalles'].append(Accesorio.objects.get(id_accesorio = d[1]))
        
        return context
    
# ------------------------- #
# Excel                     #
# ------------------------- #

class DescargarExcelTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "vistas/descargarExcel.html"

    def get(self, request, *args, **kwargs):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return super(DescargarExcelTemplateView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

    def reportes_totales(request):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return ReportesExcel.reportes(request)
        else:
            return Login.verificar_permisos_rol(permiso, request)
    def reportes_mes(self):
        return ReportesExcel.reportes_mes(self)
    def reportes_persona(self):
        return ReportesExcel.reportes_persona(self)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context