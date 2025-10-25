from django.urls import path
from . import views

app_name = 'empresas'

urlpatterns = [
    path('', views.lista_empresas, name='lista_empresas'),
    path('agregar/',views.agregar_empresa, name='agregar_empresa'),
    path('toggle/<int:empresa_id>/', views.toggle_activo, name='toggle_activo'),
    path('editar/<int:empresa_id>/', views.editar_empresa, name='editar_empresa'),
    path('eliminar/<int:empresa_id>/', views.eliminar_empresa, name='eliminar_empresa')
]