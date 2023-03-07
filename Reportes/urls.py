from django.urls import path
from . import views

app_name = 'reportesMaqman'

urlpatterns = [
    path(''                          , views.HomeTemplateView.as_view()            , name = 'home'),
    path('Inicio-Sesión/'            , views.LoginFormView.as_view()               , name = 'login'),
    path('Cerrar-Sesión/'            , views.LogoutView.as_view()                  , name = 'logout'),

    path('Perfil/'                   , views.PerfilTemplateView.as_view()          , name = 'perfil'),
    path('Vista-Principal/'          , views.PrincipalTemplateView.as_view()       , name = 'vistaPrincipal'),

    path('Generar-Report/'           , views.GenerarReportFormView.as_view()       , name = 'generarReport'),
    path('Ver-Reportes/'             , views.VerReportListView.as_view()           , name = 'verReport'),
    path('Detalle-Reporte/<int:pk>/' , views.DetalleReportDetailView.as_view()     , name = 'detalleReport'),

    path('Gestión-Usuarios/'         , views.GestionUsuarioFormView.as_view()      , name = 'gestionUsuario'),
    path('Detalle-Usuario/<int:pk>/' , views.DetalleUsuarioFormView.as_view()      , name = 'detalleUsuario'),
    path('Reporte-Usuario/<int:pk>/' , views.GestionUsuarioFormView.reporte_excel  , name = 'descargarReporte'),

    path('Descargar-Reportes/' , views.DescargarExcelTemplateView.as_view()        , name = 'descargarReport'),
    path('reporteTotal'        , views.DescargarExcelTemplateView.reportes_totales , name = 'reporteTotal'),
    path('reportePersona'      , views.DescargarExcelTemplateView.reportes_persona , name = 'reportePersona'),
    path('reporteMes'          , views.DescargarExcelTemplateView.reportes_mes     , name = 'reporteMes'),
]