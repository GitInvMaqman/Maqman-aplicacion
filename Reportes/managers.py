#----------------------------------------------------------------------------------------------------------------#
# Importaciones necesarias
#----------------------------------------------------------------------------------------------------------------#

from multiprocessing.dummy import Manager
from django.db import models
from django.db.models import Q

#----------------------------------------------------------------------------------------------------------------#
# Managers
#----------------------------------------------------------------------------------------------------------------#
class PersonaManager(models.Manager):
    def crear_persona(self, Nombres, apellidoPaterno, apellidoMaterno, Celular, Correo, Imagen, **extra_fields):
        if Correo == None:
            Correo = ''
        persona = self.create(
            nombres          = Nombres,
            apellido_paterno = apellidoPaterno,
            apellido_materno = apellidoMaterno,
            celular = Celular,
            correo = Correo,
            imagen = Imagen,
            **extra_fields
        )
        return persona

class UsuarioManager(models.Manager):
    # Permite crear un nuevo Usuario.
    def crear_usuario(self,idPersona, nombreUsuario, contraseñaUsuario, idRol, rutUsuario, **extra_fields):
        usuario = self.create(
            p_id_persona        = idPersona,
            nombre_usuario      = nombreUsuario,
            contraseña_usuario  = contraseñaUsuario,
            r_id_rol            = idRol,
            is_active           = 1,
            rut_usuario         = rutUsuario,
            **extra_fields
        )
        return usuario
    # Usuario
    def datos_por_rut(self, rutUsuario):
        return self.filter(
                rut_usuario = rutUsuario
        ).values_list()

    def traer_datos_usuario(self, nomUsuario, contraseña):
        return self.filter(
            nombre_usuario      = nomUsuario,
            contraseña_usuario  = contraseña
        ).values_list()

    def usuario_exists_1(self, rutUsuario):
        return self.filter(
            rut_usuario = rutUsuario
        ).exists()

    def usuario_exists_2(self, nombreUsuario, contraseñaUsuario):
        return self.filter(
            nombre_usuario      = nombreUsuario,
            contraseña_usuario  = contraseñaUsuario
        ).exists()

class RolManager(models.Manager):
    
    def is_rol_nombre(self, rol_id):
        return self.all().filter(
            Q(rol="Operador") | Q(rol="Asistente") | Q(rol="Mecánico") | Q(rol="Jefe")
        ).filter(
            id_rol = rol_id
        ).exists()

    def crear_rol(self, nombreRol, **extra_fields):
        rol = self.create(
            rol = nombreRol,
            **extra_fields,
        )
        return rol

    def traer_datos_rol(self):
        return self.all()
    
class ReporteManager(models.Manager):
    # Permite crear un nuevo reporte.
    def crear_reporte(self, Cliente, Obra, Fecha, HoraIngreso, HoraTermino, HorometroInicial, HorometroFinal, EquipoNumero, HorasArriendo, Observaciones, IdPersona, horometroTotal, horaMinima, imgMaquina, imgReporte, **extra_fields):
        
        reporte = self.create(
            cliente           = Cliente,
            obra              = Obra,
            fecha             = Fecha,
            hora_ingreso      = HoraIngreso,
            hora_termino      = HoraTermino,
            horometro_inicial = HorometroInicial,
            horometro_final   = HorometroFinal,
            equipo_numero     = EquipoNumero,
            horas_arriendo    = HorasArriendo,
            observaciones     = Observaciones,
            u_p_id_persona    = IdPersona,
            horometro_total   = horometroTotal,
            hora_minima       = horaMinima,
            img_maquinaria    = imgMaquina,
            img_report        = imgReporte,
            valido = 0,
            **extra_fields
        )
        return reporte
    
class DetalleManager(models.Manager):
    def crear_detalle(self, idAccesorio, idReporte, **extra_fields):
        detalle = self.create(
            a_id_accesorio = idAccesorio,
            r_id_reporte   = idReporte,
            **extra_fields
        )
        return detalle
    
class ContactoManager(models.Manager):
    def crear_contacto(self, Nombre, Correo, Empresa, Cargo, Celular, **extra_fields):

        contacto = self.create(
            nombre  = Nombre,
            correo  = Correo,
            empresa = Empresa,
            cargo   = Cargo,
            celular = Celular,
            **extra_fields
        )
        return contacto

class CorreoManager(models.Manager):
    def crear_correo(self, Asunto, Cuerpo, tipoEnvio, Fecha, Hora, **extra_fields):

        correo = self.create(
            asunto             = Asunto,
            cuerpo             = Cuerpo,
            tipo_envio_id_tipo = tipoEnvio,
            fecha              = Fecha,
            hora               = Hora,
            **extra_fields
        )
        return correo
    
class CorreoContactoManager(models.Manager):
    def crear_detalle(self, contacto, correo, **extra_fields):
        correoContacto = self.create(
            contacto_id_contacto = contacto,
            correo_id_correo     = correo,
            **extra_fields
        )
        return correoContacto

class CorreoImagenManager(models.Manager):
    def agregar_imagen(self, imagen, correo, **extra_fields):
        correoImagen = self.create(
            imagen           = imagen,
            correo_id_correo = correo,
            **extra_fields
        )
        return correoImagen

class CorreoArchivoManager(models.Manager):
    def agregar_archivo(self, archivo, correo, **extra_fields):
        correoArchivo = self.create(
            archivo          = archivo,
            correo_id_correo = correo,
            **extra_fields
        )
        return correoArchivo

class CheckMaquinaManager(models.Manager):
    def agregar_checks(self, **extra_fields):
        # correoArchivo = self.create(
        #     archivo          = archivo,
        #     correo_id_correo = correo,
        #     **extra_fields
        # )
        # return correoArchivo
        pass

class InspeccionManager(models.Manager):
    def agregar_inspeccion(self, **extra_fields):
        # correoArchivo = self.create(
        #     archivo          = archivo,
        #     correo_id_correo = correo,
        #     **extra_fields
        # )
        # return correoArchivo
        pass

class MantencionManager(models.Manager):
    def agregar_mantencion(self, **extra_fields):
        # correoArchivo = self.create(
        #     archivo          = archivo,
        #     correo_id_correo = correo,
        #     **extra_fields
        # )
        # return correoArchivo
        pass

