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

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class HomeTemplateView(TemplateView):
    template_name = "principal/home.html"
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Inicio y cierre de Sesión #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class LoginFormView(FormView):
    template_name = "principal/login.html"
    form_class    = LoginForm

    # Validación de los datos para su posterior inicio de sesión
    def form_valid(self, form):
        nomUsuario = form.cleaned_data['nombre_usuario']
        contraseña = form.cleaned_data['contraseña_usuario']
        usuario    = Usuario.objects.usuario_exists(nomUsuario, contraseña)
        return Login.login_autenticacion(self, usuario, nomUsuario, contraseña)
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class LogoutView(View):
    def get(self, request):
        return Login.cerrar_sesion(self, request)
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Usuario                   #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class PerfilTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "principal/perfil.html"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class PrincipalTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "principal/vista-principal.html"
    

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class GestionUsuarioFormView(LoginRequiredMixin, FormView):
    model               = Persona
    form_class          = PersonaForm
    template_name       = "usuarios/crudUsuario.html"
    context_object_name = "persona"
    success_url         = reverse_lazy("reportesMaqman:gestionUsuario")

    def get(self, request, *args, **kwargs):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return super(GestionUsuarioFormView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

    # Validación del formulario y posterior creación del usuario.
    def form_valid(self, form):
        datos    = form.cleaned_data
        nUsuario = self.request.POST.get('nombre_usuario')
        cUsuario = self.request.POST.get('contraseña_usuario')
        idRol    = self.request.POST.get('rol')
        usuarioExist = Usuario.objects.filter(nombre_usuario = nUsuario)
        if usuarioExist:
            titulo = '<h2>¡Usuario ya existe!</h2>'
            texto = '<p style="font-size:24;">El nombre de usuario ya está asignado a alguien más, intenta poner otro nombre de usuario.</p>'
            messages.error(self.request, titulo+texto)
            return super().form_invalid(form)
        else:
            personaCreada = ModificacionesTablas.crear_persona(self.request, datos)
            ModificacionesTablas.crear_usuario(self.request, personaCreada, nUsuario, cUsuario, idRol)
            return super(GestionUsuarioFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['nombres']  = self.request.user.p_id_persona.nombres.split()
        context["usuarios"] = Usuario.objects.order_by('-is_active', 'r_id_rol')
        context["roles"]    = Rol.objects.all()
        return context
    
    def reporte_excel(request, pk):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return ReportesExcel.reporte_operador(request, pk)
        else:
            return Login.verificar_permisos_rol(permiso, request)
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class DetalleUsuarioFormView(LoginRequiredMixin, DetailView):
    model               = Usuario
    template_name       = "usuarios/detalleUsuario.html"
    context_object_name = "usuario"
    form_class = PersonaForm
    success_url = reverse_lazy("reportesMaqman:gestionUsuario")

    def get(self, request, *args, **kwargs):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return super(DetalleUsuarioFormView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context["roles"]      = Rol.objects.all()
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

    def editar_usuario(request):
        return ModificacionesTablas.editar_usuario(request)
    
    def cambiar_activo(request):
        return ModificacionesTablas.cambiar_activo(request)
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Reportes                  #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class GenerarReportFormView(LoginRequiredMixin, FormView):
    model         = Reporte
    form_class    = ReporteForm
    template_name = "reportes/generarReport.html"
    success_url   = reverse_lazy("reportesMaqman:generarReport")

    # Validación del formulario y posterior creación de tarea.
    def form_valid(self, form):
        datos      = form.cleaned_data
        idPersona  = self.request.POST.get('p_id_persona')
        imgMaquina = self.request.FILES.get('img_maquinaria')
        imgReport  = self.request.FILES.get('img_report')
        lista      = self.request.POST.getlist('accesorios')

        reporteCreado = ModificacionesTablas.crear_reporte(self.request, datos, idPersona, imgMaquina, imgReport)
        if lista:
            ModificacionesTablas.crear_detalle(lista, reporteCreado)

        return super(GenerarReportFormView, self).form_valid(form)

    # Formulario inválido.
    def form_invalid(self, form):
        print(form.errors)
        self.request.session['acusete'] = 'form inválido'
        return super(GenerarReportFormView, self).form_invalid(form)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        context["accesorios"] = Accesorio.objects.all()
        context["operadores"] = Usuario.objects.filter(r_id_rol = 1)
        return context
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class VerReportListView(LoginRequiredMixin, ListView):
    model               = Reporte
    paginate_by         = 12
    template_name       = "reportes/verReport.html"
    context_object_name = "reportes"

    def get_queryset(self):
        if self.request.user.r_id_rol.rol == "Operador":
            return Reporte.objects.filter(u_p_id_persona = self.request.user).order_by('-fecha')
        return Reporte.objects.all().order_by('-fecha')

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class DetalleReportDetailView(LoginRequiredMixin, DetailView):
    model               = Reporte
    template_name       = "reportes/detalleReport.html"
    context_object_name = "reporte"
    

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        idReporte             = self.object.id_reporte
        context               = super().get_context_data(**kwargs)
        context["accesorios"] = Accesorio.objects.all()
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        context["operadores"] = Usuario.objects.filter(r_id_rol = 1)
        # Se obtienen los accesorios seleccionados en el reporte.
        detalle               = AccesorioReporte.objects.filter(r_id_reporte = idReporte).values_list()
        context['detalles']   = []
        for d in detalle:
            context['detalles'].append(Accesorio.objects.get(id_accesorio = d[1]))
        return context
    
    def editar_report(request):
        return ModificacionesTablas.editar_report(request)
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Excel                     #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class DescargarExcelTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "reportes/descargarExcel.html"

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
    def reportes_mes(request):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return ReportesExcel.reportes_mes(request)
        else:
            return Login.verificar_permisos_rol(permiso, request)
    def reportes_persona(request):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'
        if permiso == rol:
            return ReportesExcel.reportes_persona(request)
        else:
            return Login.verificar_permisos_rol(permiso, request)

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context