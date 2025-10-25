from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'user_first_name', 'user_last_name', 'empresa', 'rol', 'activo', 'fecha_creacion']
    list_filter = ['empresa', 'rol', 'activo']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'empresa__nombre']
    list_editable = ['activo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    # Custom methods to display user fields
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'Nombre'
    
    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Apellido'