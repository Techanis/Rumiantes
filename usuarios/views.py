from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario
from .forms import PerfilUsuarioForm
from .decorators import admin_required, coadmin_required, puede_editar_usuario

@coadmin_required
def lista_usuarios(request):
    """Lista usuarios - Solo admin+ pueden ver, filtrado por empresa"""
    if request.user.perfil.es_superadmin:
        usuarios = PerfilUsuario.objects.all()
    else:
        usuarios = PerfilUsuario.objects.filter(empresa=request.user.perfil.empresa)
    
    context = {
        'usuarios': usuarios
    }
    return render(request, 'usuarios/lista_usuarios.html', context)

@coadmin_required
def agregar_usuario(request):
    """Agregar usuario - Solo admin+ pueden agregar"""
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request=request)
        if form.is_valid():
            # Para no-superadmins, asignar su empresa automáticamente
            if not request.user.perfil.es_superadmin:
                form.instance.empresa = request.user.perfil.empresa
            form.save()
            return redirect('usuarios:lista_usuarios')
    else:
        form = PerfilUsuarioForm(request=request)
        # Para no-superadmins, forzar su empresa
        if not request.user.perfil.es_superadmin:
            form.fields['empresa'].initial = request.user.perfil.empresa
            form.fields['empresa'].disabled = True
    
    context = {
        'form': form
    }
    return render(request, 'usuarios/agregar_usuario.html', context)


@puede_editar_usuario
def editar_usuario(request, usuario_id):
    """Editar usuario - Permisos específicos por rol"""
    usuario = get_object_or_404(PerfilUsuario, id=usuario_id)
    
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=usuario, request=request)
        if form.is_valid():
            form.save()
            return redirect('usuarios:lista_usuarios')
    else:
        form = PerfilUsuarioForm(instance=usuario, request=request)
    
    context = {
        'form': form,
        'usuario': usuario
    }
    return render(request, 'usuarios/editar_usuario.html', context)


@puede_editar_usuario
def toggle_activo_usuario(request, usuario_id):
    """Activar/desactivar usuario - Mismos permisos que editar"""
    usuario = get_object_or_404(PerfilUsuario, id=usuario_id)
    usuario.activo = not usuario.activo
    usuario.save()
    return redirect('usuarios:lista_usuarios')

@admin_required
@puede_editar_usuario
def eliminar_usuario(request, usuario_id):
    """Eliminar usuario - Solo admin+ con permisos específicos"""
    usuario = get_object_or_404(PerfilUsuario, id=usuario_id)
    if request.method == 'POST':
        usuario.user.delete()
    return redirect('usuarios:lista_usuarios')