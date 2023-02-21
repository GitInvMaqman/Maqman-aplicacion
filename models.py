# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accesorio(models.Model):
    id_accesorio = models.AutoField(primary_key=True)
    accesorio_minicargador = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'accesorio'


class AccesorioReporte(models.Model):
    r_id_reporte = models.OneToOneField('Reporte', models.DO_NOTHING, db_column='r_id_reporte', primary_key=True)
    a_id_accesorio = models.ForeignKey(Accesorio, models.DO_NOTHING, db_column='a_id_accesorio')

    class Meta:
        managed = False
        db_table = 'accesorio_reporte'
        unique_together = (('r_id_reporte', 'a_id_accesorio'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=30)
    apellido_materno = models.CharField(max_length=30)
    celular = models.CharField(max_length=12, blank=True, null=True)
    correo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persona'


class Reporte(models.Model):
    id_reporte = models.BigAutoField(primary_key=True)
    cliente = models.CharField(max_length=100)
    obra = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_ingreso = models.DateTimeField()
    hora_termino = models.DateTimeField()
    horometro_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    horometro_final = models.DecimalField(max_digits=10, decimal_places=2)
    horas_arriendo = models.DecimalField(max_digits=4, decimal_places=2)
    horometro_total = models.DecimalField(max_digits=10, decimal_places=2)
    hora_minima = models.DecimalField(max_digits=4, decimal_places=2)
    equipo_numero = models.CharField(max_length=50)
    observaciones = models.CharField(max_length=1024)
    img_maquinaria = models.BinaryField(blank=True, null=True)
    img_report = models.BinaryField(blank=True, null=True)
    u_p_id_persona = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='u_p_id_persona')

    class Meta:
        managed = False
        db_table = 'reporte'


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class Usuario(models.Model):
    p_id_persona = models.OneToOneField(Persona, models.DO_NOTHING, db_column='p_id_persona', primary_key=True)
    nombre_usuario = models.CharField(max_length=50)
    contraseña_usuario = models.CharField(max_length=50)
    r_id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='r_id_rol')

    class Meta:
        managed = False
        db_table = 'usuario'
