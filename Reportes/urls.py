from django.urls import path
from . import views

app_name = 'reportesMaqman'

urlpatterns = [
    path(''                          , views.HomeTemplateView.as_view()             , name = 'home'),
    path('Inicio-Sesión/'            , views.LoginFormView.as_view()                , name = 'login'),
    path('Cerrar-Sesión/'            , views.LogoutView.as_view()                   , name = 'logout'),

    path('Perfil/'                   , views.PerfilTemplateView.as_view()           , name = 'perfil'),
    path('Vista-Principal/'          , views.PrincipalTemplateView.as_view()        , name = 'vistaPrincipal'),

    path('Generar-Report/'           , views.GenerarReportFormView.as_view()        , name = 'generarReport'),
    path('Ver-Reportes/'             , views.VerReportListView.as_view()            , name = 'verReport'),
    path('Detalle-Reporte/<int:pk>/' , views.DetalleReportDetailView.as_view()      , name = 'detalleReport'),
    path('Editar-Reporte/'           , views.DetalleReportDetailView.editar_report  , name = 'editarReport'),
    path('Validar-Reporte/'          , views.DetalleReportDetailView.validar_report , name = 'validarReport'),

    path('Gestión-Usuarios/'         , views.GestionUsuarioFormView.as_view()       , name = 'gestionUsuario'),
    path('Detalle-Usuario/<int:pk>/' , views.DetalleUsuarioFormView.as_view()       , name = 'detalleUsuario'),
    path('Reporte-Usuario/<int:pk>/' , views.GestionUsuarioFormView.reporte_excel   , name = 'descargarReporte'),
    path('Editar-Usuario/'           , views.DetalleUsuarioFormView.editar_usuario  , name = 'editarUsuario'),
    path('Cambiar-Activo/'           , views.DetalleUsuarioFormView.cambiar_activo  , name = 'cambiarActivo'),

    path('Descargar-Reportes/' , views.DescargarExcelTemplateView.as_view()         , name = 'descargarReport'),
    path('reporteTotal'        , views.DescargarExcelTemplateView.reportes_totales  , name = 'reporteTotal'),
    path('reportePersona'      , views.DescargarExcelTemplateView.reportes_persona  , name = 'reportePersona'),
    path('reporteMes'          , views.DescargarExcelTemplateView.reportes_mes      , name = 'reporteMes'),

    # Correos automáticos
    path('Vista-Correos/'            , views.CorreosTemplateView.as_view()          , name = 'vistaCorreos'),
    path('Gestion-Contactos/'        , views.ContactosFormView.as_view()            , name = 'gestionContactos'),
    path('Programar-Correo/'         , views.CorreoFormView.as_view()               , name = 'programarCorreo'),
    path('Correos-Programados/'      , views.CorreosListView.as_view()              , name = 'correosProgramados'),
    path('Detalle-Correo/<int:pk>/'  , views.CorreoDetailView.as_view()             , name = 'detalleCorreo'),
    
    path('Pruebas/', views.PruebasView.as_view(), name = 'pruebas'),
]