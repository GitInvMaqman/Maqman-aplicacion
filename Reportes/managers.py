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
    def crear_persona(self, Nombres, apellidoPaterno, apellidoMaterno, Celular, Correo, **extra_fields):
        if Correo == None:
            Correo = ''
        persona = self.create(
            nombres          = Nombres,
            apellido_paterno = apellidoPaterno,
            apellido_materno = apellidoMaterno,
            celular = Celular,
            correo = Correo,
            **extra_fields
        )
        return persona
class UsuarioManager(models.Manager):
    # Permite crear un nuevo Usuario.
    def crear_usuario(self,idPersona, nombreUsuario, contraseñaUsuario, idRol, **extra_fields):
        usuario = self.create(
            p_id_persona        = idPersona,
            nombre_usuario      = nombreUsuario,
            contraseña_usuario  = contraseñaUsuario,
            r_id_rol            = idRol,
            is_active = 1,
            **extra_fields
        )
        return usuario
    # Usuario
    def traer_datos_usuario(self, username, password):
        return self.filter(
            nombre_usuario      = username,
            contraseña_usuario  = password
        ).values_list()

    def usuario_exists(self, nombreUsuario, contraseñaUsuario):
        return self.filter(
            nombre_usuario      = nombreUsuario,
            contraseña_usuario  = contraseñaUsuario
        ).exists()

class RolManager(models.Manager):
    
    def is_rol_nombre(self, rol_id):
        return self.all().filter(
            Q(rol="Operador") | Q(rol="Asistente") | Q(rol="Administrador")
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