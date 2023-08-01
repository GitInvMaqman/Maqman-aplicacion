from django.db import models
from .managers import *

# Create your models here.
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    rol    = models.CharField(max_length=50, blank=True, null=True)

    objects = RolManager()

    def init(self,  id_rol):
       self.p_id_rol= id_rol

    class Meta:
        managed  = False
        db_table = 'rol'


class Persona(models.Model):
    id_persona       = models.AutoField(primary_key=True)
    nombres          = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    celular          = models.IntegerField(blank=True, null=True)
    correo           = models.CharField(max_length=50, blank=True, null=True)
    imagen           = models.ImageField(upload_to="imagen_perfil", null=True)

    objects = PersonaManager()

    def init(self,  id_persona):
       self.p_id_persona= id_persona

    class Meta:
        managed  = False
        db_table = 'persona'

class Usuario(models.Model):
    p_id_persona       = models.OneToOneField(Persona, models.DO_NOTHING, db_column='p_id_persona', primary_key=True)
    nombre_usuario     = models.CharField(max_length=50)
    contraseña_usuario = models.CharField(max_length=50)
    r_id_rol           = models.ForeignKey(Rol, models.DO_NOTHING, db_column='r_id_rol')
    last_login         = models.DateTimeField()
    is_active          = models.IntegerField()
    is_authenticated   = True
    rut_usuario        = models.CharField(max_length=10)

    objects = UsuarioManager()

    def init(self,  id_usuario):
       self.p_id_usuario= id_usuario

    class Meta:
        managed  = False
        db_table = 'usuario'


class Reporte(models.Model):
    id_reporte        = models.BigAutoField(primary_key=True)
    cliente           = models.CharField(max_length=100)
    obra              = models.CharField(max_length=100)
    fecha             = models.DateField()
    hora_ingreso      = models.TimeField()
    hora_termino      = models.TimeField()
    horometro_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    horometro_final   = models.DecimalField(max_digits=10, decimal_places=2)
    horas_arriendo    = models.DecimalField(max_digits=4, decimal_places=2)
    horometro_total   = models.DecimalField(max_digits=10, decimal_places=2)
    hora_minima       = models.DecimalField(max_digits=4, decimal_places=2)
    equipo_numero     = models.CharField(max_length=50)
    observaciones     = models.CharField(max_length=1024)
    img_maquinaria    = models.ImageField(upload_to="maquinas", null=True)
    img_report        = models.ImageField(upload_to="reportes", null=True)
    u_p_id_persona    = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='u_p_id_persona')
    valido            = models.IntegerField()

    objects = ReporteManager()

    def init(self,  id_reporte):
       self.id_reporte= id_reporte

    class Meta:
        managed  = False
        db_table = 'reporte'

class Accesorio(models.Model):
    id_accesorio           = models.AutoField(primary_key=True)
    accesorio_minicargador = models.CharField(max_length=50)

    def init(self,  id_accesorio):
       self.p_id_accesorio= id_accesorio

    class Meta:
        managed  = False
        db_table = 'accesorio'


class AccesorioReporte(models.Model):
    r_id_reporte   = models.OneToOneField('Reporte', models.DO_NOTHING, db_column='r_id_reporte', primary_key=True)
    a_id_accesorio = models.ForeignKey(Accesorio, models.DO_NOTHING, db_column='a_id_accesorio')

    objects = DetalleManager()

    class Meta:
        managed  = False
        db_table = 'accesorio_reporte'
        unique_together = (('r_id_reporte', 'a_id_accesorio'),)

# ------------------------------------------------------------------------------------------------------------------------
# Sistema de Correo Automático
# ------------------------------------------------------------------------------------------------------------------------

class Contacto(models.Model):
    id_contacto = models.BigAutoField(primary_key=True)
    nombre      = models.CharField(max_length=50)
    correo      = models.CharField(max_length=100)
    empresa     = models.CharField(max_length=50)
    cargo       = models.CharField(max_length=50)
    celular     = models.IntegerField(blank=True, null=True)

    objects = ContactoManager()

    class Meta:
        managed  = False
        db_table = 'contacto'

class Correo(models.Model):
    id_correo          = models.BigAutoField(primary_key=True)
    asunto             = models.CharField(max_length=100)
    cuerpo             = models.CharField(max_length=2048)
    tipo_envio_id_tipo = models.ForeignKey('TipoEnvio', models.DO_NOTHING, db_column='tipo_envio_id_tipo')
    fecha              = models.DateField()
    hora               = models.DateTimeField()

    objects = CorreoManager()

    class Meta:
        managed  = False
        db_table = 'correo'

class CorreoContacto(models.Model):
    contacto_id_contacto = models.OneToOneField(Contacto, models.DO_NOTHING, db_column='contacto_id_contacto', primary_key=True)
    correo_id_correo     = models.ForeignKey(Correo, models.DO_NOTHING, db_column='correo_id_correo')

    objects = CorreoContactoManager()
    class Meta:
        managed  = False
        db_table = 'correo_contacto'
        unique_together = (('contacto_id_contacto', 'correo_id_correo'),)

class TipoEnvio(models.Model):
    id_tipo = models.SmallAutoField(primary_key=True)
    tipo    = models.CharField(max_length=20)

    class Meta:
        managed  = False
        db_table = 'tipo_envio'

class ImagenCorreo(models.Model):
    id_imagen        = models.AutoField(primary_key=True)
    imagen           = models.ImageField(upload_to="imagenes_correos", null=True)
    correo_id_correo = models.ForeignKey(Correo, models.DO_NOTHING, db_column='correo_id_correo')

    objects = CorreoImagenManager()
    class Meta:
        managed  = False
        db_table = 'imagen_correo'

class ArchivoCorreo(models.Model):
    id_archivo       = models.AutoField(primary_key=True)
    archivo          = models.FileField(upload_to="archivos_correos", null=True)
    correo_id_correo = models.ForeignKey('Correo', models.DO_NOTHING, db_column='correo_id_correo')

    objects = CorreoArchivoManager()

    class Meta:
        managed  = False
        db_table = 'archivo_correo'

# ------------------------------------------------------------------------------------------------------------------------
# Mantención
# ------------------------------------------------------------------------------------------------------------------------

class Checkmaquina(models.Model):
    id_check = models.BigAutoField(primary_key=True)
    check_1  = models.BooleanField()
    check_2  = models.BooleanField()
    check_3  = models.BooleanField()
    check_4  = models.BooleanField()
    check_5  = models.BooleanField()
    check_6  = models.BooleanField()
    check_7  = models.BooleanField()
    check_8  = models.BooleanField()
    check_9  = models.BooleanField()
    check_10 = models.BooleanField()
    check_11 = models.BooleanField()
    check_12 = models.BooleanField()
    check_13 = models.BooleanField()
    check_14 = models.BooleanField()
    check_15 = models.BooleanField()

    objects = CheckMaquinaManager()
    class Meta:
        managed  = False
        db_table = 'checkmaquina'


class Inspeccion(models.Model):
    id_inspeccion   = models.BigAutoField(primary_key=True)
    m_id_mantencion = models.ForeignKey('Mantencion', models.DO_NOTHING, db_column='m_id_mantencion')
    inspeccion      = models.CharField(max_length=100)
    check1          = models.CharField(max_length=50)
    busqueda        = models.CharField(max_length=512)
    check2          = models.CharField(max_length=50)
    estado          = models.CharField(max_length=512)

    objects = InspeccionManager()
    class Meta:
        managed  = False
        db_table = 'inspeccion'


class Mantencion(models.Model):
    id_mantencion   = models.BigAutoField(primary_key=True)
    u_p_id_persona  = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='u_p_id_persona')
    fecha           = models.DateField()
    numero_maquina  = models.CharField(max_length=20)
    horometro_maq   = models.DecimalField(max_digits=10, decimal_places=1)
    ch_id_check     = models.ForeignKey(Checkmaquina, models.DO_NOTHING, db_column='ch_id_check')
    descripcion     = models.CharField(max_length=1024)
    observacion     = models.CharField(max_length=1024)
    insumos         = models.CharField(max_length=512)
    prox_mantencion = models.CharField(max_length=200)
    prox_horometro  = models.DecimalField(max_digits=10, decimal_places=1)
    archivo         = models.CharField(max_length=200)

    objects = MantencionManager()
    class Meta:
        managed  = False
        db_table = 'mantencion'

