#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

import os
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

import threading
import time
import datetime
from dateutil.relativedelta import relativedelta

#----------------------------------------------------------------------------------------------------------------#
# Funciones
#----------------------------------------------------------------------------------------------------------------#

class Timer(threading.Thread):
    def __init__(self):
        self._timer_runs = threading.Event()
        self._timer_runs.set()
        super().__init__()

    def run(self):
        while self._timer_runs.is_set():
            self.timer()
            time.sleep(self.__class__.interval)

    def stop(self):
        self._timer_runs.clear()

class Login():

# Mensaje de alerta por si existen problemas con el login.
    def problemas_login(self, problema):
        titulo = '<h2>No se ha podido iniciar sesión</h2>'
        texto = '<p style="font-size:24px;">' + problema + '</p>'
        messages.error(self.request, titulo+texto)
        return HttpResponseRedirect(reverse('reportesMaqman:login-1'))

# Ingreso del usuario a través del rut.
    def login_rut(self, usuario, rutUsuario):
        if not usuario:
            problema = 'Verifica que el rut está correctamente ingresado.'
            return Login.problemas_login(self, problema)

        activo = Usuario.objects.datos_por_rut(rutUsuario)[0][5]

        if not activo:
            problema = 'Esta cuenta ya no está activa, contáctate con la empresa o intenta iniciar sesión con otra cuenta.'
            return Login.problemas_login(self, problema)
        
        rol_id = Usuario.objects.datos_por_rut(rutUsuario)[0][3]
        is_rol = Rol.objects.is_rol_nombre(rol_id)
        # Si el rol del usuario no existe en la base de datos manda un mensaje de alerta, de lo contrario continúa.
        if not is_rol:
            problema = 'El rol de esta cuenta no existe, contáctate con la empresa o intenta iniciar sesión con otra cuenta.'
            return Login.problemas_login(self, problema)

        rol = Rol.objects.filter(id_rol = rol_id)[0]
        if rol.rol == "Operador" or rol.rol == "Mecánico":
            nomUsuario = Usuario.objects.datos_por_rut(rutUsuario)[0][1]
            contraseña = Usuario.objects.datos_por_rut(rutUsuario)[0][2]

            autUsuario = authenticate(username=nomUsuario, password=contraseña)
            # Si la autenticación del usuario es negada manda un mensaje de alerta, de lo contrario continúa.
            if autUsuario is None:
                problema = 'La autenticación del usuario ha sido negada, contáctate con la empresa o intenta iniciar sesión con otra cuenta.'
                return Login.problemas_login(self, problema)

            login(self.request, autUsuario) # Guarda la información para no tener que loguearse en cada instante.

            rol       = self.request.user.r_id_rol.rol
            nombre    = self.request.user.p_id_persona.nombres.split()
            redirect_to = 'reportesMaqman:vistaPrincipal'

            titulo = '<h2>Has iniciado sesión como '+ rol.upper() + ': '+ nombre[0] +'</h2>'
            texto = '<p style="font-size:24px;">¡Inicio de sesión exitoso!</p>'
            messages.success(self.request,titulo+texto)

            return HttpResponseRedirect(reverse(redirect_to))
        elif rol_id == 2:
            redirect_to = 'reportesMaqman:login-2'

            titulo = '<h2>Inicio de sesión Administrativo.</h2>'
            texto = '<p style="font-size:24px;">Como miembro administrativo de la empresa, debes ingresar tu nombre de usuario y contraseña para una mayor seguridad.</p>'
            messages.success(self.request,titulo+texto)

            return HttpResponseRedirect(reverse(redirect_to))
        else:
            problema = 'Existe un problema actualmente y no es posible iniciar sesión.'
            return Login.problemas_login(self, problema)

# Autenticación de usuario al loguearse.
    def login_autenticacion(self, usuario, nomUsuario, contraseña):
        # Si el usuario no existe manda un mensaje de alerta, de lo contrario continúa.
        if not usuario:
            problema = 'Verifica que la "Contraseñas" y/o el "Usuario" sean los correctos.'
            return Login.problemas_login(self, problema)

        activo = Usuario.objects.traer_datos_usuario(nomUsuario, contraseña)[0][5]

        if not activo:
            problema = 'Esta cuenta ya no está activa, contáctate con la empresa o intenta iniciar sesión con otra cuenta.'
            return Login.problemas_login(self, problema)

        rol_id = Usuario.objects.traer_datos_usuario(nomUsuario, contraseña)[0][3]
        is_rol = Rol.objects.is_rol_nombre(rol_id)
        # Si el rol del usuario no existe en la base de datos manda un mensaje de alerta, de lo contrario continúa.
        if not is_rol:
            problema = 'El rol de esta cuenta no existe, contáctate con la empresa o intenta iniciar sesión con otra cuenta.'
            return Login.problemas_login(self, problema)

        autUsuario = authenticate(username=nomUsuario, password=contraseña)
        # Si la autenticación del usuario es negada manda un mensaje de alerta, de lo contrario continúa.
        if autUsuario is None:
            problema = 'La autenticación del usuario ha sido negada, contáctate con la empresa o intenta iniciar sesión con otra cuenta.'
            return Login.problemas_login(self, problema)

        login(self.request, autUsuario) # Guarda la información para no tener que loguearse en cada instante.

        rol       = self.request.user.r_id_rol.rol
        nombre    = self.request.user.p_id_persona.nombres.split()
        redirect_to = 'reportesMaqman:vistaPrincipal'

        titulo = '<h2>Has iniciado sesión como '+ rol.upper() + ': '+ nombre[0] +'</h2>'
        texto = '<p style="font-size:24px;">¡Inicio de sesión exitoso!</p>'
        messages.success(self.request,titulo+texto)

        return HttpResponseRedirect(reverse(redirect_to))

# Verificación de los permisos según el rol para ingresar a ciertas páginas.
    def verificar_permisos_rol(rol, request):
        titulo = '<h2>Eres ' + rol.upper() + '</h2>'
        texto = '<p style="font-size:24px;">No posees los permisos necesarios para ingresar a esta página.</p>'
        messages.warning(request, titulo+texto)
        return HttpResponseRedirect(reverse('reportesMaqman:vistaPrincipal'))

# Cerrado de sesión con su respectivo mensaje de alerta y redirección.
    def cerrar_sesion(sel, request):
        logout(request)
        titulo = '<h2>Se ha cerrado la sesión correctamente.</h2>'
        messages.success(request, titulo)
        return HttpResponseRedirect(reverse('reportesMaqman:login-1'))
    
class ModificacionesTablas():

    def problemas_correos(request, titulo, texto):
            messages.error(request, titulo+texto)
            error = False
            return error

    def crear_correo(request, form):
        # Se comprueba si se ingresó al menos un contacto.
        contactos  = request.POST.getlist('checkbox')
        if not contactos:
            titulo = '<h2>¡No hay contactos seleccionados!</h2>'
            texto = '<p style="font-size:24;">Se necesita ingresar al menos un contacto para poder programar un correo.</p>'
            return ModificacionesTablas.problemas_correos(request, titulo, texto)
        
        # Se comprueba si se ingresó algún tipo de envío.
        tipoEnvio  = request.POST.get('tipo_envio')
        if not tipoEnvio:
            titulo = '<h2>¡No hay algún tipo de envío seleccionado!</h2>'
            texto = '<p style="font-size:24;">Se necesita ingresar algún tipo de envío para poder programar un correo.</p>'
            return ModificacionesTablas.problemas_correos(request, titulo, texto)

        # Se registra la fecha y hora según el tipo de envío.
        fecha = ""
        hora = ""
        # Tipo Anual.
        if tipoEnvio == "1":
            dia = request.POST.get('diaAnual')
            mes = request.POST.get('mesAnual')
            hrs = request.POST.get('horaAnual')
            fecha = "1998-" + mes + "-" + dia
        # Tipo Mensual.
        elif tipoEnvio == "2":
            dia = request.POST.get("diaMensual")
            hrs = request.POST.get('horaMensual')
            fecha = "1998-10-" + dia
        # Tipo Semanal.
        elif tipoEnvio == "3":
            dia = request.POST.get("diaSemanal")
            hrs = request.POST.get('horaSemanal')
            fecha = "1998-10-0" + dia
        # Tipo Único.
        elif tipoEnvio == "4":
            fecha = request.POST.get("fechaUnica")
            hrs = request.POST.get('horaUnica')

        # Si se registró la hora se registra como fecha con hora y se registra el tipo de envío.
        if hrs:
            hora = "1998-10-08 " + hrs
            envio = TipoEnvio.objects.filter(id_tipo = tipoEnvio)

        # Se comprueba si se ingresó la fecha.
        if not fecha:
            titulo = '<h2>¡No hay fecha ingresada!</h2>'
            texto = '<p style="font-size:24;">Se necesita ingresar alguna fecha para poder programar un correo.</p>'
            return ModificacionesTablas.problemas_correos(request, titulo, texto)

        # Se comprueba si se ingresó la hora.
        if not hora:
            titulo = '<h2>¡No hay hora ingresada!</h2>'
            texto = '<p style="font-size:24;">Se necesita ingresar alguna hora para poder programar un correo.</p>'
            return ModificacionesTablas.problemas_correos(request, titulo, texto)

        # Se registran los datos necesarios para programar un correo.
        datos      = form.cleaned_data
        correoCreado = Correo.objects.crear_correo(
            datos['asunto'],
            datos['cuerpo'],
            envio[0],
            fecha,
            hora,
        )

        # Se agregan los contactos al correo programado.
        ModificacionesTablas.agregar_contactos(request, contactos, correoCreado)

        # Se ingresan las imagenes en una lista y luego se agregan al correo programado si se ingresaron anteriormente.
        imagen = request.FILES.getlist('img')
        if imagen:
            ModificacionesTablas.agregar_imagenes(request, imagen, correoCreado)

        # Se ingresan los archivos en una lista y luego se agregan al correo programado si se ingresaron anteriormente.
        archivo = request.FILES.getlist('archivo')
        if archivo:
            ModificacionesTablas.agregar_archivos(request, archivo, correoCreado)

# Agregar Mensaje preguntando si está seguro de ingresar esos datos.
        titulo = '<h2>¡Correo programado exitosamente!</h2>'
        messages.success(request, titulo)
        return correoCreado
    def agregar_contactos(request, contactos, correo):
        lista = []
        for idContacto in contactos:
            contactos[contactos.index(idContacto)] = int(idContacto)
            contacto = Contacto.objects.get(id_contacto = idContacto)
            detContactoCorreo = CorreoContacto.objects.crear_detalle(contacto, correo)
            lista.append(detContactoCorreo)
        return lista
    def agregar_imagenes(request, imagenes, correo):
        lista = []
        for imagen in imagenes:
            imagenCorreo = ImagenCorreo.objects.agregar_imagen(imagen, correo)
            lista.append(imagenCorreo)
        return lista
    def agregar_archivos(request, archivos, correo):
        lista = []
        for archivo in archivos:
            archivoCorreo = ArchivoCorreo.objects.agregar_archivo(archivo, correo)
            lista.append(archivoCorreo)
        return lista

    def editar_correo(request):
        pass

    def crear_contacto(request, datos):
        contactoCreado = Contacto.objects.crear_contacto(
            datos['nombre'],
            datos['correo'],
            datos['empresa'],
            datos['cargo'],
            datos['celular'],
        )
        titulo = '<h2>Contacto N° '+ str(contactoCreado.id_contacto) +' creado exitosamente!</h2>'
        messages.success(request, titulo)
        return contactoCreado

    def editar_contacto(request):
        idContacto = request.POST.get('id_contacto')
        Nombre     = request.POST.get('nombre')
        Correo     = request.POST.get('correo')
        Empresa    = request.POST.get('empresa')
        Cargo      = request.POST.get('cargo')
        Celular    = request.POST.get('celular')

        contacto = Contacto.objects.get(id_contacto = idContacto)

        contacto.nombre   = Nombre
        contacto.correo   = Correo
        contacto.empresa  = Empresa
        contacto.cargo    = Cargo
        contacto.celular  = Celular

        contacto.save()

        titulo = '<h2>¡Contacto actualizado!</h2>'
        texto  = '<p style="font-size:24;">Los datos del contacto se han editado exitosamente.</p>'
        messages.success(request, titulo+texto)
        return HttpResponseRedirect('/Gestion-Contactos/')
    
    def borrar_contacto(request, id):
        contacto = Contacto.objects.get(id_contacto=id)
        contacto.delete()
        messages.success(request, 'El contacto se ha borrado con éxito')
        return HttpResponseRedirect(reverse('reportesMaqman:gestionContactos'))

    def crear_reporte(request, datos, idPersona, imgMaquina, imgReport):
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
            imgMaquina,
            imgReport,
        )
        titulo = '<h2>Reporte N° '+ str(reporteCreado.id_reporte) +' creado exitosamente!</h2>'
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
    
    def editar_report(request):
        id_report         = request.POST.get('id_report')
        cliente           = request.POST.get('cliente')
        obra              = request.POST.get('obra')
        fecha             = request.POST.get('fecha')
        hora_ingreso      = request.POST.get('hora_ingreso')
        hora_termino      = request.POST.get('hora_termino')
        horas_arriendo    = request.POST.get('horas_arriendo')
        horometro_inicial = request.POST.get('horometro_inicial')
        horometro_final   = request.POST.get('horometro_final')
        horometro_total   = request.POST.get('horometro_total')
        equipo_numero     = request.POST.get('equipo_numero')
        hora_minima       = request.POST.get('hora_minima')
        observaciones     = request.POST.get('observaciones')
        p_id_persona      = request.POST.get('p_id_persona')

        lista             = request.POST.getlist('accesorios')

        accesorios = Accesorio.objects.all()
        for a in accesorios:
            detalle = AccesorioReporte.objects.filter(r_id_reporte = id_report, a_id_accesorio = a)
            if detalle:
                detalle.delete()

        img_maquinaria    = request.FILES.get('img_maquinaria')
        img_report        = request.FILES.get('img_report')

        reporte = Reporte.objects.get(id_reporte = id_report)
        usuario = Usuario.objects.get(p_id_persona = p_id_persona)
        # persona = Persona.objects.get(id_persona = usuario.p_id_persona.id_persona)

        reporte.cliente           = cliente
        reporte.obra              = obra
        reporte.fecha             = fecha
        reporte.hora_ingreso      = hora_ingreso
        reporte.hora_termino      = hora_termino
        reporte.horas_arriendo    = horas_arriendo
        reporte.horometro_inicial = horometro_inicial
        reporte.horometro_final   = horometro_final
        reporte.horometro_total   = horometro_total
        reporte.equipo_numero     = equipo_numero
        reporte.hora_minima       = hora_minima
        reporte.observaciones     = observaciones
        reporte.u_p_id_persona    = usuario

        dirImgMaquinaria = os.path.join(settings.MEDIA_ROOT+'/'+reporte.img_maquinaria.name)
        dirImgReport = os.path.join(settings.MEDIA_ROOT+'/'+reporte.img_report.name)

        if lista:
            ModificacionesTablas.crear_detalle(lista, reporte)

        if img_maquinaria == None:
            img_maquinaria = reporte.img_maquinaria
        elif reporte.img_maquinaria == '':
            print('hola')
        else:
            os.remove(dirImgMaquinaria)

        if img_report == None:
            img_report = reporte.img_report
        elif reporte.img_report == '':
            print('hola')
        else:
            os.remove(dirImgReport)

        reporte.img_maquinaria    = img_maquinaria
        reporte.img_report        = img_report

        reporte.save()

        titulo = '<h2>¡Reporte actualizado!</h2>'
        texto  = '<p style="font-size:24;">Los datos del reporte se han editado exitosamente.</p>'
        messages.success(request, titulo+texto)
        return HttpResponseRedirect('/Detalle-Reporte/' + id_report)
    
    def validar_report(request):
        idReport = request.POST.get('id_report')
        reporte  = Reporte.objects.get(id_reporte = idReport)

        if reporte.valido == 0:
            reporte.valido = 1
            validez        = 'validado'
            if reporte.img_maquinaria != '':
                os.remove(os.path.join(settings.MEDIA_ROOT+'/'+reporte.img_maquinaria.name))
                reporte.img_maquinaria = ''
            if reporte.img_report != '':
                os.remove(os.path.join(settings.MEDIA_ROOT+'/'+reporte.img_report.name))
                reporte.img_report = ''
        else:
            reporte.valido = 0
            validez        = 'invalidado'

        reporte.save()

        titulo = '<h2>¡Reporte ' + validez + '!</h2>'
        texto  = '<p style="font-size:24;">El reporte se ha '+ validez + ' con éxito.</p>'
        messages.success(request, titulo+texto)
        return HttpResponseRedirect('/Ver-Reportes/')

    def crear_persona(request, datos, imagen):
        personaCreada = Persona.objects.crear_persona(
            datos['nombres'],
            datos['apellido_paterno'],
            datos['apellido_materno'],
            datos['celular'],
            datos['correo'],
            imagen,
        )
        return personaCreada
    def crear_usuario(request, idPersona, nUsuario, cUsuario, idRol, rutUsuario):
        rol = Rol(idRol)
        usuarioCreado = Usuario.objects.crear_usuario(
            idPersona,
            nUsuario,
            cUsuario,
            rol,
            rutUsuario,
        )
        persona = usuarioCreado.p_id_persona
        titulo = '<h2>El usuario "'+ persona.nombres + ' ' + persona.apellido_paterno + ' ' + persona.apellido_materno +'"</h2>'
        texto = '<p style="font-size:24px;">¡ha sido creado exitosamente!</p>'
        messages.success(request, titulo + texto)
        return usuarioCreado

    def editar_usuario(request):
        tipo         = request.POST.get('tipo')
        idPersona    = request.POST.get('id_persona')
        uNombre      = request.POST.get('nombre_usuario')
        usuario      = Usuario.objects.get(p_id_persona = idPersona)
        usuarioExist = Usuario.objects.filter(nombre_usuario = uNombre)
        uRUT         = usuario.rut_usuario

        if usuarioExist:
            if usuario != usuarioExist[0]:
                titulo = '<h2>¡Usuario ya existe!</h2>'
                texto  = '<p style="font-size:24;">El nombre de usuario ya está asignado a alguien más, intenta poner otro nombre de usuario.</p>'
                messages.error(request, titulo+texto)
                if tipo == 'perfil':
                    return HttpResponseRedirect('/Perfil/')
                else:
                    return HttpResponseRedirect('/Detalle-Usuario/'+idPersona)
        if tipo == 'detalle':
            uRUT = request.POST.get('rut_usuario')
            rutExist = Usuario.objects.filter(rut_usuario = uRUT)
            if rutExist:
                if usuario != rutExist[0]:
                    titulo = '<h2>¡El rut ya existe!</h2>'
                    texto  = '<p style="font-size:24;">El rut ya está asignado a alguien más, intenta poner otro rut.</p>'
                    messages.error(request, titulo+texto)
                    if tipo == 'perfil':
                        return HttpResponseRedirect('/Perfil/')
                    else:
                        return HttpResponseRedirect('/Detalle-Usuario/'+idPersona)

        persona = usuario.p_id_persona

        pNombres  = request.POST.get('nombres')
        pAPaterno = request.POST.get('apellido_paterno')
        pAMaterno = request.POST.get('apellido_materno')
        pCelular  = request.POST.get('celular')
        pCorreo   = request.POST.get('correo')

        if pCelular == '':
            pCelular = None
        if pCorreo == 'None':
            pCorreo = ''

        imgPerfil = request.FILES.get('img_perfil')
        if imgPerfil == None:
            imgPerfil = persona.imagen
        elif persona.imagen == '' or persona.imagen == None:
            print('hola')
        else:
            dirImgPerfil = os.path.join(settings.MEDIA_ROOT+'/'+persona.imagen.name)
            os.remove(dirImgPerfil)

        persona.imagen           = imgPerfil
        persona.nombres          = pNombres
        persona.apellido_paterno = pAPaterno
        persona.apellido_materno = pAMaterno
        persona.celular          = pCelular
        persona.correo           = pCorreo
        persona.save()

        uContraseña = request.POST.get('contraseña_usuario')
        idRol       = request.POST.get('rol')
        rRol        = Rol.objects.get(id_rol = idRol)

        usuario.nombre_usuario     = uNombre
        usuario.contraseña_usuario = uContraseña
        usuario.r_id_rol           = rRol
        usuario.rut_usuario        = uRUT

        
        usuario.save()
        if tipo == 'perfil':
            titulo = '<h2>¡Perfil actualizado!</h2>'
            texto  = '<p style="font-size:24;">Los datos de tu perfil se han editado con éxito.</p>'
            messages.success(request, titulo+texto)
            return HttpResponseRedirect('/Perfil/')
        else:
            titulo = '<h2>¡Usuario actualizado!</h2>'
            texto  = '<p style="font-size:24;">Los datos del usuario se han editado con éxito.</p>'
            messages.success(request, titulo+texto)
            return HttpResponseRedirect('/Detalle-Usuario/'+idPersona)
    
    def cambiar_activo(request):
        idPersona    = request.POST.get('id_persona')
        usuario      = Usuario.objects.get(p_id_persona = idPersona)
        persona      = usuario.p_id_persona

        if usuario.is_active == 0:
            usuario.is_active = 1
            activo = 'activado'
        else:
            usuario.is_active = 0
            activo = 'desactivado'
            if persona.imagen:
                os.remove(os.path.join(settings.MEDIA_ROOT+'/'+persona.imagen.name))
                persona.imagen = ''
                persona.save()

        usuario.save()

        titulo = '<h2>¡Usuario ' + activo + '!</h2>'
        texto  = '<p style="font-size:24;">El usuario se ha '+ activo + ' con éxito.</p>'
        messages.success(request, titulo+texto)
        # return HttpResponseRedirect('/Detalle-Usuario/'+idPersona)
        return HttpResponseRedirect('/Gestión-Usuarios/')

    def crear_mantencion(request, datos):
        checks = {}
        for i in range(1,16):
            check = request.POST.get(f'check_{i}')
            if check == None:
                check = False
            else:
                check = True
            checks[f'check_{i}'] = check
        checkmaquina = ModificacionesTablas.crear_checkmaquina(checks)
        usuario = Usuario.objects.get(p_id_persona = request.POST.get('p_id_persona'))
        mantencion = Mantencion.objects.agregar_mantencion(
            usuario,
            datos['fecha'],
            datos['numero_maquina'],
            datos['horometro_maq'],
            checkmaquina,
            datos['descripcion'],
            datos['observacion'],
            datos['insumos'],
            datos['prox_mantencion'],
            datos['prox_horometro'],
            request.FILES.get('img_mantencion')
        )
        return mantencion
    def crear_checkmaquina(checks):
        checkMaquinacreado = Checkmaquina.objects.agregar_checks(
            checks['check_1'],
            checks['check_2'],
            checks['check_3'],
            checks['check_4'],
            checks['check_5'],
            checks['check_6'],
            checks['check_7'],
            checks['check_8'],
            checks['check_9'],
            checks['check_10'],
            checks['check_11'],
            checks['check_12'],
            checks['check_13'],
            checks['check_14'],
            checks['check_15']
        )
        return checkMaquinacreado
    def crear_inspeccion(request, mantencion):
        listaInspecciones = []
        for i in range(1,32):
            inspeccionCreada = Inspeccion.objects.agregar_inspeccion(
                mantencion,
                request.POST.get(f'inspeccion{i}'),
                request.POST.get(f'chk1_{i}'),
                request.POST.get(f'busqueda{i}'),
                request.POST.get(f'chk2_{i}'),
                request.POST.get(f'estado{i}')
            )
            
            listaInspecciones.append(inspeccionCreada)
            titulo = '<h2>¡Mantención creada!</h2>'
            texto  = '<p style="font-size:24;">El certificado de mantención del minicargador se ha creado con éxito.</p>'
            messages.success(request, titulo+texto)
        return listaInspecciones

    def editar_mantencion(request):
        mantencion   = Mantencion.objects.get(id_mantencion = request.POST.get('id_mantencion'))
        checkMaq     = Checkmaquina.objects.get(id_check = mantencion.ch_id_check.id_check)
        inspecciones = Inspeccion.objects.filter(m_id_mantencion = mantencion.id_mantencion).order_by('id_inspeccion')
        persona      = Usuario.objects.get(p_id_persona = request.POST.get('p_id_persona'))

        for i in range(0, 31):
            print(inspecciones[i])
            print(inspecciones)
            inspeccion = inspecciones[i]
            inspeccion.inspeccion = request.POST.get(f'inspeccion{i+1}')
            inspeccion.check1     = request.POST.get(f'chk1_{i+1}')
            inspeccion.busqueda   = request.POST.get(f'busqueda{i+1}')
            inspeccion.check2     = request.POST.get(f'chk2_{i+1}')
            inspeccion.estado     = request.POST.get(f'estado{i+1}')

            inspeccion.save()

        checks = {}
        for i in range(1,16):
            check = request.POST.get(f'check_{i}')
            if check == None:
                check = False
            else:
                check = True
            checks[f'check_{i}'] = check

        checkMaq.check_1  = checks['check_1']
        checkMaq.check_2  = checks['check_2']
        checkMaq.check_3  = checks['check_3']
        checkMaq.check_4  = checks['check_4']
        checkMaq.check_5  = checks['check_5']
        checkMaq.check_6  = checks['check_6']
        checkMaq.check_7  = checks['check_7']
        checkMaq.check_8  = checks['check_8']
        checkMaq.check_9  = checks['check_9']
        checkMaq.check_10 = checks['check_10']
        checkMaq.check_11 = checks['check_11']
        checkMaq.check_12 = checks['check_12']
        checkMaq.check_13 = checks['check_13']
        checkMaq.check_14 = checks['check_14']
        checkMaq.check_15 = checks['check_15']
        
        checkMaq.save()

        mantencion.u_p_id_persona  = persona
        mantencion.fecha           = request.POST.get('fecha')
        mantencion.numero_maquina  = request.POST.get('numero_maquina')
        mantencion.horometro_maq   = request.POST.get('horometro_maq')
        mantencion.descripcion     = request.POST.get('descripcion')
        mantencion.observacion     = request.POST.get('observacion')
        mantencion.insumos         = request.POST.get('insumos')
        mantencion.prox_mantencion = request.POST.get('prox_mantencion')
        mantencion.prox_horometro  = request.POST.get('prox_horometro')
        
        archivoMantencion = request.FILES.get('img_mantencion')

        dirArchivoMantencion = os.path.join(settings.MEDIA_ROOT+'/'+mantencion.archivo.name)

        if archivoMantencion == None:
            archivoMantencion = mantencion.archivo
        elif mantencion.archivo == '':
            print('hola')
        else:
            os.remove(dirArchivoMantencion)

        mantencion.archivo = archivoMantencion

        mantencion.save()

        titulo = '<h2>¡Mantención actualizada!</h2>'
        texto  = '<p style="font-size:24;">Los datos del certificado se han editado con éxito.</p>'
        messages.success(request, titulo+texto)
        return HttpResponseRedirect('/Detalle-Mantencion/' + request.POST.get('id_mantencion'))

    def validar_mantencion(request):
        idMantencion = request.POST.get('id_mantencion')
        mantencion   = Mantencion.objects.get(id_mantencion = idMantencion)

        if mantencion.valido == 0:
            mantencion.valido = 1
            validez        = 'validada'
            if mantencion.archivo != '':
                os.remove(os.path.join(settings.MEDIA_ROOT+'/'+mantencion.archivo.name))
                mantencion.archivo = ''
        else:
            mantencion.valido = 0
            validez        = 'invalidada'

        mantencion.save()

        titulo = '<h2>¡Mantención ' + validez + '!</h2>'
        texto  = '<p style="font-size:24;">La mantención se ha '+ validez + ' con éxito.</p>'
        messages.success(request, titulo+texto)
        return HttpResponseRedirect('/Ver-Mantenciones/')

class operacionesFechas():
    def reporte_mes(mes):
        reportes = Reporte.objects.filter(valido = 1).order_by('fecha')
        listaReportes = []
        for r in reportes:
            fechaReporte = r.fecha.month
            if fechaReporte == mes:
                listaReportes.append(r)
        return listaReportes

class EnvioCorreos():
    def envio(asunto, content, contactos, archivos, imagenes):
        email = EmailMultiAlternatives(
            asunto,
            None,
            settings.EMAIL_HOST_USER,
            contactos
        )
        email.attach_alternative(content, 'text/html')
        if archivos:
            for archivo in archivos:
                email.attach(archivo.name.split('/')[-1], archivo.read(), archivo.name)
        if imagenes:
            for imagen in imagenes:
                email.attach(imagen.name.split('/')[-1], imagen.read(), imagen.name)

        email.fail_silently = False
        email.send()
        return HttpResponseRedirect('/Vista-Correos/')

    def correo(correo, asunto, cuerpo, archivos, imagenes, tipoEnvio, fecha, contactos):
        template = get_template('email_template01.html')
        context = {
                'asunto': asunto,
                'cuerpo': cuerpo,
                'archivos': archivos,
                'imagenes': imagenes
            }
        content = template.render(context)
        print(archivos)
        print(imagenes)

        # envio = EnvioCorreos.envio(asunto, content, ["ccm.abarca.tecnologica@gmail.com"])
        envio = EnvioCorreos.envio(asunto, content, contactos, archivos, imagenes)

        # # Tipo Anual.
        # if tipoEnvio == 1:
        #     fecha += relativedelta(years=1)
        # # Tipo Mensual.
        # elif tipoEnvio == 2:
        #     fecha += relativedelta(months=1)
        # # Tipo Semanal.
        # elif tipoEnvio == 3:
        #     fecha += datetime.timedelta(weeks=1)
        # # Tipo Único.
        # elif tipoEnvio == 4:
        #     pass
        # print(fecha)
        # print("------------------")
        # print(fecha.strftime("%Y-%m-%d"))
        # nuevaFecha =fecha.strftime("%Y-%m-%d")
        # print("------------------")
        # print(nuevaFecha)
        # print("------------------")
        # correo.fecha = nuevaFecha
        # correo.save()

        return envio