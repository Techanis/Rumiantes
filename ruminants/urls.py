from django.urls import path
from . import views

app_name = 'ruminants'

urlpatterns = [
    path('', views.lista_ruminants, name='lista_ruminants'),
    path('agregar/', views.agregar_ruminant, name='agregar_ruminant'),
    path('editar/<int:ruminant_id>/', views.editar_ruminant, name='editar_ruminant'),
    path('eliminar/<int:ruminant_id>/', views.eliminar_ruminant, name='eliminar_ruminant'),
    path('iot-data/', views.lista_iot_data, name='lista_iot_data'),
    path('alertas/',views.lista_alerta,name='lista_alerta'),
    path('reportes/',views.reporte,name='reportes'),
]