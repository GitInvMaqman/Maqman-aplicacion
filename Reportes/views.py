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
    template_name = "principal/sitio-maqman.html"
    # template_name = "principal/home.html"
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Inicio y cierre de Sesión #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# Inicio de sesión por rut del usuario.
class Login1FormView(FormView):
    template_name = "principal/login-1.html"
    form_class    = Login1Form

    # Validación de los datos para su posterior inicio de sesión
    def form_valid(self, form):
        rutUsuario = form.cleaned_data['rut_usuario']
        usuario    = Usuario.objects.usuario_exists_1(rutUsuario)
        return Login.login_rut(self, usuario, rutUsuario)

# Inicio de sesión por nombre y contraseña del usuario.
class Login2FormView(FormView):
    template_name = "principal/login-2.html"
    form_class    = Login2Form

    # Validación de los datos para su posterior inicio de sesión
    def form_valid(self, form):
        nomUsuario = form.cleaned_data['nombre_usuario']
        contraseña = form.cleaned_data['contraseña_usuario']
        usuario    = Usuario.objects.usuario_exists_2(nomUsuario, contraseña)
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

class PrincipalView(LoginRequiredMixin, TemplateView):
    template_name = "principal/vista-principal.html"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

class ReportesView(LoginRequiredMixin, TemplateView):
    template_name = "principal/vista-reportes.html"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

class CorreosView(LoginRequiredMixin, TemplateView):
    template_name = "principal/vista-correos.html"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
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

class VerReportesView(LoginRequiredMixin, TemplateView):
    template_name = "reportes/ver-reportes.html"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context               = super().get_context_data(**kwargs)
        context['nombres']    = self.request.user.p_id_persona.nombres.split()
        return context

class ReportesValidosListView(LoginRequiredMixin, ListView):
    model               = Reporte
    paginate_by         = 20
    template_name       = "reportes/reportes.html"
    context_object_name = "reportes"

    def get_queryset(self):
        if self.request.user.r_id_rol.rol == "Operador":
            return Reporte.objects.filter(u_p_id_persona = self.request.user, valido = 0).order_by('-fecha')
        return Reporte.objects.filter(valido = 0).order_by('-fecha')

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context

class ReportesInvalidosListView(LoginRequiredMixin, ListView):
    model               = Reporte
    paginate_by         = 20
    template_name       = "reportes/reportes.html"
    context_object_name = "reportes"

    def get_queryset(self):
        if self.request.user.r_id_rol.rol == "Operador":
            return Reporte.objects.filter(u_p_id_persona = self.request.user, valido = 0).order_by('-fecha')
        return Reporte.objects.filter(valido = 1).order_by('-fecha')

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
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

    def validar_report(request):
        return ModificacionesTablas.validar_report(request)

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

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Correos automatizados     #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

class ContactosFormView(LoginRequiredMixin, FormView):
    model               = Contacto
    form_class          = ContactoForm
    template_name       = "autocorreos/gestion-contacto.html"
    success_url         = reverse_lazy("reportesMaqman:gestionContactos")

    def get(self, request, *args, **kwargs):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'  #Cambiar por jefe y/o admin
        if permiso == rol:
            return super(ContactosFormView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

    # Validación del formulario y posterior creación del usuario.
    def form_valid(self, form):
        datos    = form.cleaned_data
        ModificacionesTablas.crear_contacto(self.request, datos)
        return super(ContactosFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['nombres']  = self.request.user.p_id_persona.nombres.split()
        context["contacto"] = Contacto.objects.all()
        return context

    def editar_contacto(request):
        return ModificacionesTablas.editar_contacto(request)
    
    def borrar_contacto(request, id):
        return ModificacionesTablas.borrar_contacto(request, id)

class CorreoFormView(LoginRequiredMixin, FormView):
    model               = Correo
    form_class          = CorreoForm
    template_name       = "autocorreos/programar-correo.html"
    success_url         = reverse_lazy("reportesMaqman:programarCorreo")

    def get(self, request, *args, **kwargs):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'  #Cambiar por jefe y/o admin
        if permiso == rol:
            return super(CorreoFormView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)

    # Validación del formulario y posterior programación del correo.
    def form_valid(self, form):
        valido = super(CorreoFormView, self).form_valid(form)
        correo = ModificacionesTablas.crear_correo(self.request, form)

        if correo == False:
            valido = super().form_invalid(form)

        return valido

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['nombres']  = self.request.user.p_id_persona.nombres.split()
        context["contacto"] = Contacto.objects.all()
        context["envios"]   = TipoEnvio.objects.all()
        context["dias"]     = range(1,32)
        context["semana"]   = {1:"Lunes", 2:"Martes", 3:"Miércoles", 4:"Jueves", 5:"Viernes", 6:"Sábado", 7:"Domingo", }
        context['meses']    = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        return context

    def enviarCorreo(self):
        correo    = Correo.objects.all()[0]
        idCorreo  = correo.id_correo
        asunto    = correo.asunto
        cuerpo    = correo.cuerpo
        tipoEnvio = correo.tipo_envio_id_tipo.id_tipo
        fecha     = correo.fecha

        archivos = ArchivoCorreo.objects.filter(correo_id_correo = idCorreo).values_list()
        listaArchivos = []
        for archivo in archivos:
            listaArchivos.append(archivo[1])
        imagenes = ImagenCorreo.objects.filter(correo_id_correo = idCorreo).values_list()
        listaImagenes = []
        for imagen in imagenes:
            listaImagenes.append(imagen[1])
        contactos = CorreoContacto.objects.filter(correo_id_correo = idCorreo).values_list()
        listaContactos = []
        for contacto in contactos:
            persona = Contacto.objects.get(id_contacto = contacto[0])
            correoContacto = persona.correo
            listaContactos.append(correoContacto)
        print(f"archivos: {listaArchivos}")
        print(f"imagenes: {listaImagenes}")
        print(f"contactos: {listaContactos}")
        Enviar = EnvioCorreos.correo(correo, asunto, cuerpo, listaArchivos, listaImagenes, tipoEnvio, fecha, listaContactos)
        return Enviar

class CorreosListView(LoginRequiredMixin, ListView):
    model               = Correo
    paginate_by         = 20
    template_name       = "autocorreos/correos-programados.html"
    context_object_name = "correos"

    def get(self, request, *args, **kwargs):
        permiso = request.user.r_id_rol.rol
        rol     = 'Asistente'  #Cambiar por jefe y/o admin
        if permiso == rol:
            return super(CorreosListView, self).get(request, *args, **kwargs)
        else:
            return Login.verificar_permisos_rol(permiso, request)
    # def get_queryset(self):
    #     return Reporte.objects.all().order_by('valido', '-fecha')

    # Obtención de otros datos.
    def get_context_data(self, *args, **kwargs):
        context            = super().get_context_data(**kwargs)
        context['nombres'] = self.request.user.p_id_persona.nombres.split()
        return context

class CorreoDetailView(LoginRequiredMixin, DetailView):
    model               = Correo
    template_name       = "autocorreos/detalle-correo.html"
    context_object_name = "correo"

    # Obtención de otros datos.
    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['nombres']  = self.request.user.p_id_persona.nombres.split()
        context["contacto"] = Contacto.objects.all()
        context["envios"]   = TipoEnvio.objects.all()
        context["dias"]     = range(1,32)
        context["semana"]   = {1:"Lunes", 2:"Martes", 3:"Miércoles", 4:"Jueves", 5:"Viernes", 6:"Sábado", 7:"Domingo", }
        context['meses']    = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        return context

    # def editar_report(request):
    #     return ModificacionesTablas.editar_report(request)

    # def validar_report(request):
    #     return ModificacionesTablas.validar_report(request)

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Reportes Mecánicos        #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# class AgregarMantenimientoView(LoginRequiredMixin, FormView):
#     model         = Mantenimiento
#     form_class    = MantenimientoForm
#     template_name = "mantenimiento/generar-mantenimiento.html"
#     success_url   = reverse_lazy("reportesMaqman:generarMantenimiento")

#     # Validación del formulario y posterior creación de tarea.
#     def form_valid(self, form):
#         datos      = form.cleaned_data
#         idPersona  = self.request.POST.get('p_id_persona')
#         imgMaquina = self.request.FILES.get('img_maquinaria')
#         imgReport  = self.request.FILES.get('img_report')
#         lista      = self.request.POST.getlist('accesorios')

#         reporteCreado = ModificacionesTablas.crear_reporte(self.request, datos, idPersona, imgMaquina, imgReport)
#         if lista:
#             ModificacionesTablas.crear_detalle(lista, reporteCreado)

#         return super(GenerarReportFormView, self).form_valid(form)

#     # Formulario inválido.
#     def form_invalid(self, form):
#         print(form.errors)
#         return super(GenerarReportFormView, self).form_invalid(form)

#     # Obtención de otros datos.
#     def get_context_data(self, *args, **kwargs):
#         context               = super().get_context_data(**kwargs)
#         context['nombres']    = self.request.user.p_id_persona.nombres.split()
#         context["accesorios"] = Accesorio.objects.all()
#         context["operadores"] = Usuario.objects.filter(r_id_rol = 1)
#         return context
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# class VerReportListView(LoginRequiredMixin, ListView):
#     model               = Reporte
#     paginate_by         = 20
#     template_name       = "reportes/verReport.html"
#     context_object_name = "reportes"

#     def get_queryset(self):
#         if self.request.user.r_id_rol.rol == "Operador":
#             return Reporte.objects.filter(u_p_id_persona = self.request.user, valido = 0).order_by('-fecha')
#         return Reporte.objects.all().order_by('valido', '-fecha')

#     # Obtención de otros datos.
#     def get_context_data(self, *args, **kwargs):
#         context            = super().get_context_data(**kwargs)
#         context['nombres'] = self.request.user.p_id_persona.nombres.split()
#         return context
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# class DetalleReportDetailView(LoginRequiredMixin, DetailView):
#     model               = Reporte
#     template_name       = "reportes/detalleReport.html"
#     context_object_name = "reporte"

#     # Obtención de otros datos.
#     def get_context_data(self, **kwargs):
#         idReporte             = self.object.id_reporte
#         context               = super().get_context_data(**kwargs)
#         context["accesorios"] = Accesorio.objects.all()
#         context['nombres']    = self.request.user.p_id_persona.nombres.split()
#         context["operadores"] = Usuario.objects.filter(r_id_rol = 1)
#         # Se obtienen los accesorios seleccionados en el reporte.
#         detalle               = AccesorioReporte.objects.filter(r_id_reporte = idReporte).values_list()
#         context['detalles']   = []
#         for d in detalle:
#             context['detalles'].append(Accesorio.objects.get(id_accesorio = d[1]))
#         return context

#     def editar_report(request):
#         return ModificacionesTablas.editar_report(request)

#     def validar_report(request):
#         return ModificacionesTablas.validar_report(request)
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Excel                     #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# class DescargarExcelTemplateView(LoginRequiredMixin, TemplateView):
#     template_name = "reportes/descargarExcel.html"

#     def get(self, request, *args, **kwargs):
#         permiso = request.user.r_id_rol.rol
#         rol     = 'Asistente'
#         if permiso == rol:
#             return super(DescargarExcelTemplateView, self).get(request, *args, **kwargs)
#         else:
#             return Login.verificar_permisos_rol(permiso, request)

#     def reportes_totales(request):
#         permiso = request.user.r_id_rol.rol
#         rol     = 'Asistente'
#         if permiso == rol:
#             return ReportesExcel.reportes(request)
#         else:
#             return Login.verificar_permisos_rol(permiso, request)
#     def reportes_mes(request):
#         permiso = request.user.r_id_rol.rol
#         rol     = 'Asistente'
#         if permiso == rol:
#             return ReportesExcel.reportes_mes(request)
#         else:
#             return Login.verificar_permisos_rol(permiso, request)
#     def reportes_persona(request):
#         permiso = request.user.r_id_rol.rol
#         rol     = 'Asistente'
#         if permiso == rol:
#             return ReportesExcel.reportes_persona(request)
#         else:
#             return Login.verificar_permisos_rol(permiso, request)

#     # Obtención de otros datos.
#     def get_context_data(self, *args, **kwargs):
#         context            = super().get_context_data(**kwargs)
#         context['nombres'] = self.request.user.p_id_persona.nombres.split()
#         return context

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

# ------------------------- #
# Pruebas                   #
# ------------------------- #

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class PruebasView(LoginRequiredMixin, TemplateView):
    template_name = "prueba.html"

    def get_context_data(self, **kwargs):
        context             = super().get_context_data(**kwargs)
        context['nombres']  = self.request.user.p_id_persona.nombres.split()
        context["contacto"] = Contacto.objects.all()
        context["envios"]   = TipoEnvio.objects.all()
        return context