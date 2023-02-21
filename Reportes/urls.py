from django.urls import path
from . import views

app_name = 'reportesMaqman'

urlpatterns = [
    path(''                          , views.HomeTemplateView.as_view()          , name = 'home'),

    path('Inicio-Sesión/'            , views.LoginFormView.as_view()             , name = 'login'),
    path('Cerrar-Sesión/'            , views.LogoutView.as_view()                , name = 'logout'),

    path('Perfil/'                   , views.PerfilTemplateView.as_view()        , name = 'perfil'),

    path('Vista-Operador/'           , views.OperadorTemplateView.as_view()      , name = 'operador'),
    path('Vista-Asistente/'          , views.AsistenteTemplateView.as_view()     , name = 'asistente'),

    path('Generar-Report/'           , views.GenReportFormView.as_view()         , name = 'genReport'),
    path('Ver-Reportes/'             , views.VerReportListView.as_view()         , name = 'verReport'),
    path('Detalle-Reporte/<int:pk>/' , views.DetReportDetailView.as_view()       , name = 'detReport'),
    path('Descargar-Reportes/'       , views.DescargarExcelTemplateView.as_view(), name = 'descargarReport'),

    path('reporteTotal'      , views.DescargarExcelTemplateView.reportes_totales , name = 'reporteTotal'),
    path('reportePersona'    , views.DescargarExcelTemplateView.reportes_persona , name = 'reportePersona'),
    path('reporteMes'        , views.DescargarExcelTemplateView.reportes_mes     , name = 'reporteMes'),
]