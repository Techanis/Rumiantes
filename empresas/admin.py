from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ruc', 'telefono', 'email', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'ruc']
    list_editable = ['activo']