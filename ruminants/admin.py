from django.contrib import admin
from .models import Ruminant, ModuloIoT,IoTData

@admin.register(ModuloIoT)
class ModuloIoTAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'empresa', 'estado', 'activo']
    list_filter = ['empresa', 'estado', 'activo']
    search_fields = ['nombre', 'codigo', 'empresa__nombre']
    list_editable = ['activo']
@admin.register(Ruminant)
class RuminantAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'empresa', 'sexo', 'raza', 'activo']
    list_filter = ['empresa', 'sexo', 'estado_produccion', 'activo']
    search_fields = ['nombre', 'codigo', 'raza', 'empresa__nombre']
    list_editable = ['activo']
@admin.register(IoTData)
class IoTDataAdmin(admin.ModelAdmin):
    list_display = ("modulo_iot", "temperatura", "actividad", "latitud", "longitud", "bateria", "timestamp")
    list_filter = ("modulo_iot",)
    search_fields = ("modulo_iot__codigo",)