from django.db import models
from .managers import *

# Create your models here.
class Rol(models.Model):
    id_rol  = models.AutoField(primary_key=True)
    rol     = models.CharField(max_length=50, blank=True, null=True)

    objects = RolManager()

    def init(self,  id_rol):
       self.p_id_rol= id_rol

    class Meta:
        managed = False
        db_table = 'rol'


class Persona(models.Model):
    id_persona          = models.AutoField(primary_key=True)
    nombres             = models.CharField(max_length=50)
    apellido_paterno    = models.CharField(max_length=30)
    apellido_materno    = models.CharField(max_length=30)
    celular             = models.CharField(max_length=12, blank=True, null=True)
    correo              = models.CharField(max_length=50, blank=True, null=True)

    objects = PersonaManager()

    def init(self,  id_persona):
       self.p_id_persona= id_persona

    class Meta:
        managed     = False
        db_table    = 'persona'

class Usuario(models.Model):
    p_id_persona        = models.OneToOneField(Persona, models.DO_NOTHING, db_column='p_id_persona', primary_key=True)
    nombre_usuario      = models.CharField(max_length=50)
    contraseña_usuario  = models.CharField(max_length=50)
    r_id_rol            = models.ForeignKey(Rol, models.DO_NOTHING, db_column='r_id_rol')
    is_active           = models.BooleanField()

    # is_authenticated    = True

    objects = UsuarioManager()

    def init(self,  id_usuario):
       self.p_id_usuario= id_usuario

    class Meta:
        managed     = False
        db_table    = 'usuario'


class Reporte(models.Model):
    id_reporte          = models.BigAutoField(primary_key=True)
    cliente             = models.CharField(max_length=100)
    obra                = models.CharField(max_length=100)
    fecha               = models.DateField()
    hora_ingreso        = models.TimeField()
    hora_termino        = models.TimeField()
    horometro_inicial   = models.DecimalField(max_digits=10, decimal_places=2)
    horometro_final     = models.DecimalField(max_digits=10, decimal_places=2)
    horas_arriendo      = models.DecimalField(max_digits=4, decimal_places=2)
    horometro_total     = models.DecimalField(max_digits=10, decimal_places=2)
    hora_minima         = models.DecimalField(max_digits=4, decimal_places=2)
    equipo_numero       = models.CharField(max_length=50)
    observaciones       = models.CharField(max_length=1024)
    img_maquinaria      = models.BinaryField(blank=True, null=True)
    img_report          = models.BinaryField(blank=True, null=True)
    u_p_id_persona      = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='u_p_id_persona')

    objects = ReporteManager()

    def init(self,  id_reporte):
       self.id_reporte= id_reporte

    class Meta:
        managed     = False
        db_table    = 'reporte'

class Accesorio(models.Model):
    id_accesorio            = models.AutoField(primary_key=True)
    accesorio_minicargador  = models.CharField(max_length=50)

    def init(self,  id_accesorio):
       self.p_id_accesorio= id_accesorio

    class Meta:
        managed     = False
        db_table    = 'accesorio'


class AccesorioReporte(models.Model):
    r_id_reporte = models.OneToOneField('Reporte', models.DO_NOTHING, db_column='r_id_reporte', primary_key=True)
    a_id_accesorio = models.ForeignKey(Accesorio, models.DO_NOTHING, db_column='a_id_accesorio')

    objects = DetalleManager()

    class Meta:
        managed = False
        db_table = 'accesorio_reporte'
        unique_together = (('r_id_reporte', 'a_id_accesorio'),)