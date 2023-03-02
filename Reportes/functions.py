#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

# from django.core.mail import EmailMultiAlternatives
# from django.conf import settings

# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from io import BytesIO
# import datetime

#----------------------------------------------------------------------------------------------------------------#
# Funciones
#----------------------------------------------------------------------------------------------------------------#

class Login():

# Mensaje de alerta por si existen problemas con el login.
    def problemas_login(self):
        titulo = '<h1>No se ha podido iniciar sesión</h1>'
        texto = '<p style="font-size:24px;">Verifica que el "Usuario" y/o la "Contraseña" estén correctos.</p>'
        messages.error(self.request, titulo+texto)
        return HttpResponseRedirect(reverse('reportesMaqman:login'))

# Autenticación de usuario al loguearse.
    def login_autenticacion(self, usuario, nomUsuario, contraseña):
        # Si el usuario no existe manda un mensaje de alerta, de lo contrario continúa.
        if not usuario:
            return Login.problemas_login(self)

        rol_id = Usuario.objects.traer_datos_usuario(nomUsuario, contraseña)[0][3]
        is_rol = Rol.objects.is_rol_nombre(rol_id)
        # Si el rol del usuario no existe en la base de datos manda un mensaje de alerta, de lo contrario continúa.
        if not is_rol:
            return Login.problemas_login(self)
        
        autUsuario = authenticate(username=nomUsuario, password=contraseña)
        # Si la autenticación del usuario es negada manda un mensaje de alerta, de lo contrario continúa.
        if autUsuario is None:
            return Login.problemas_login(self)

        login(self.request, autUsuario) # Guarda la información para no tener que loguearse en cada instante.

        rol       = self.request.user.r_id_rol.rol
        nombre    = self.request.user.p_id_persona.nombres.split()
        redirect_to = 'reportesMaqman:vistaPrincipal'

        titulo = '<h1>Has iniciado sesión como '+ rol.upper() + ': '+ nombre[0] +'</h1>'
        texto = '<p style="font-size:24px;">¡Inicio de sesión exitoso!</p>'
        messages.success(self.request,titulo+texto)

        return HttpResponseRedirect(reverse(redirect_to))

# Verificación de los permisos según el rol para ingresar a ciertas páginas.
    def verificar_permisos_rol(rol, request):
        titulo = '<h1>Eres ' + rol.upper() + '</h1>'
        texto = '<p style="font-size:24px;">No posees los permisos necesarios para ingresar a esta página.</p>'
        messages.warning(request, titulo+texto)
        return HttpResponseRedirect(reverse('reportesMaqman:vistaPrincipal'))

# Cerrado de sesión con su respectivo mensaje de alerta y redirección.
    def cerrar_sesion(sel, request):
        logout(request)
        titulo = '<h1>Se ha cerrado la sesión correctamente.</h1>'
        messages.success(request, titulo)
        return HttpResponseRedirect(reverse('reportesMaqman:login'))
    
class ModificacionesTablas():

    def crear_reporte(request, datos, idPersona):
        idUsuario = Usuario(idPersona)
        reporteCreado = Reporte.objects.crear_reporte(
            datos['cliente'],
            datos['obra'],
            datos['fecha'],
            datos['hora_ingreso'],
            datos['hora_termino'],
            datos['horometro_inicial'],
            datos['horometro_final'],
            datos['equipo_numero'],
            datos['horas_arriendo'],
            datos['observaciones'],
            idUsuario,
            datos['horometro_total'],
            datos['hora_minima'],
        )
        titulo = '<h1>Reporte N° '+ str(reporteCreado.id_reporte) +' creado exitosamente!</h1>'
        messages.success(request, titulo)
        return reporteCreado
    
    def crear_detalle(lista, reporte):
        lista_detalles = []
        for idAccesorio in lista:
            lista[lista.index(idAccesorio)] = int(idAccesorio)
            accesorio = Accesorio.objects.get(id_accesorio = idAccesorio)
            detalleCreado = AccesorioReporte.objects.crear_detalle(accesorio, reporte)
            lista_detalles.append(detalleCreado)
        return lista_detalles
    
    def crear_persona(request, datos):
        personaCreada = Persona.objects.crear_persona(
            datos['nombres'],
            datos['apellido_paterno'],
            datos['apellido_materno'],
            datos['celular'],
            datos['correo'],
        )
        return personaCreada
    def crear_usuario(request, idPersona, nUsuario, cUsuario, idRol):
        rol = Rol(idRol)
        usuarioCreado = Usuario.objects.crear_usuario(
            idPersona,
            nUsuario,
            cUsuario,
            rol,
        )
        persona = usuarioCreado.p_id_persona
        titulo = '<h1>El usuario "'+ persona.nombres + ' ' + persona.apellido_paterno + ' ' + persona.apellido_materno +'"</h1>'
        texto = '<p style="font-size:24px;">¡ha sido creado exitosamente!</p>'
        messages.success(request, titulo + texto)
        return usuarioCreado

    
class operacionesFechas():
    def reporte_mes(mes):
        reportes = Reporte.objects.all().order_by('fecha')
        listaReportes = []
        for r in reportes:
            fechaReporte = r.fecha.month
            if fechaReporte == mes:
                listaReportes.append(r)
        return listaReportes

