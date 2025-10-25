from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def rol_requerido(roles_permitidos):
    """
    Decorator básico para verificar roles
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login:login')
            
            if not hasattr(request.user, 'perfil'):
                raise PermissionDenied("Usuario sin perfil")
            
            if request.user.perfil.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            
            raise PermissionDenied("No tienes permisos para acceder a esta página")
        return _wrapped_view
    return decorator

def superadmin_required(view_func):
    """Solo Super Administrador"""
    return rol_requerido(['superadmin'])(view_func)

def admin_required(view_func):
    """Super Administrador y Administrador"""
    return rol_requerido(['superadmin', 'admin'])(view_func)

def coadmin_required(view_func):
    """Super Administrador, Administrador y Co-Administrador"""
    return rol_requerido(['superadmin', 'admin', 'coadmin'])(view_func)

def usuario_required(view_func):
    """Todos los roles pueden acceder"""
    return rol_requerido(['superadmin', 'admin', 'coadmin', 'jefe'])(view_func)

# Decorators específicos para permisos de empresa
def puede_editar_usuario(view_func):
    """
    Permite editar usuarios según el rol:
    - superadmin: puede editar todos
    - admin: puede editar admin, coadmin, usuario de su empresa
    - coadmin: puede editar usuario de su empresa
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login:login')
        
        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Usuario sin perfil")
        
        # Superadmin puede editar cualquier usuario
        if request.user.perfil.es_superadmin:
            return view_func(request, *args, **kwargs)
        
        # Para otros roles, necesitamos el usuario_id del parámetro
        usuario_id = kwargs.get('usuario_id')
        if not usuario_id:
            raise PermissionDenied("ID de usuario no proporcionado")
        
        from .models import PerfilUsuario
        try:
            usuario_target = PerfilUsuario.objects.get(id=usuario_id)
        except PerfilUsuario.DoesNotExist:
            raise PermissionDenied("Usuario no encontrado")
        
        # Verificar permisos según rol
        user_perfil = request.user.perfil
        
        if user_perfil.es_admin:
            # Admin puede editar usuarios de su empresa (excepto superadmin)
            if usuario_target.empresa == user_perfil.empresa and not usuario_target.es_superadmin:
                return view_func(request, *args, **kwargs)
        
        elif user_perfil.es_coadmin:
            # Coadmin solo puede editar usuarios normales de su empresa
            if (usuario_target.empresa == user_perfil.empresa and 
                usuario_target.es_usuario):
                return view_func(request, *args, **kwargs)
        
        raise PermissionDenied("No tienes permisos para editar este usuario")
    return _wrapped_view

def mismo_empresa_required(view_func):
    """
    Verifica que el usuario acceda solo a datos de su empresa
    (a menos que sea superadmin)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login:login')
        
        if not hasattr(request.user, 'perfil'):
            raise PermissionDenied("Usuario sin perfil")
        
        # Superadmin puede ver todo
        if request.user.perfil.es_superadmin:
            return view_func(request, *args, **kwargs)
        
        # Para otros roles, aplicar filtro de empresa en la vista
        return view_func(request, *args, **kwargs)
    return _wrapped_view