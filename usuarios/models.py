from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from empresas.models import Empresa

class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('superadmin', 'Super Administrador'),
        ('admin', 'Administrador'),
        ('coadmin', 'Co-Administrador'),
        ('jefe', 'Jefe de establo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    empresa = models.ForeignKey(
        'empresas.Empresa', 
        on_delete=models.CASCADE, 
        verbose_name="Empresa"
    )
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    rol = models.CharField(
        max_length=20, 
        choices=ROL_CHOICES, 
        default='jefe',
        verbose_name="Rol del Usuario"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['user__email']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_rol_display()} - {self.empresa.nombre}"
    
    # Property methods for easy role checking
    @property
    def es_superadmin(self):
        return self.rol == 'superadmin'
    
    @property
    def es_admin(self):
        return self.rol == 'admin'
    
    @property
    def es_coadmin(self):
        return self.rol == 'coadmin'
    
    @property
    def es_usuario(self):
        return self.rol == 'jefe'
    
    # Permission methods
    @property
    def puede_crear_usuarios(self):
        return self.rol in ['superadmin', 'admin']
    
    @property
    def puede_editar_usuarios(self):
        return self.rol in ['superadmin', 'admin', 'coadmin']
    
    @property
    def puede_eliminar_usuarios(self):
        return self.rol in ['superadmin', 'admin']
    
    @property
    def puede_gestionar_empresas(self):
        return self.rol in ['superadmin']
    
    @property
    def puede_gestionar_ruminants(self):
        return self.rol in ['superadmin', 'admin', 'coadmin', 'jefe']

