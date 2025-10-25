from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import superadmin_required
from .models import Empresa
from .forms import EmpresaForm

@login_required
@superadmin_required
def lista_empresas(request):
    empresas = Empresa.objects.all()
    context = {
        'empresas': empresas
    }
    return render(request, 'empresas/lista_empresas.html', context)

def agregar_empresa(request):
    if request.method== 'POST':
        form_empresa = EmpresaForm(request.POST)
        if form_empresa.is_valid():
            form_empresa.save()
            print("Datos recibidos", form_empresa)
            return redirect('empresas:lista_empresas')
    else:
        form_empresa = EmpresaForm()
         
    context = {
        'form': form_empresa
    }
    return render(request, 'empresas/agregar_empresa.html', context)

def toggle_activo(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.activo = not empresa.activo
    empresa.save()
    return redirect('empresas:lista_empresas')

def editar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('empresas:lista_empresas')
    else:
        form = EmpresaForm(instance=empresa)  # Pre-fill with current data
    
    context = {
        'form': form,
        'empresa': empresa
    }
    return render(request, 'empresas/editar_empresa.html', context)

def eliminar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    if request.method == 'POST':
        empresa.delete()
        return redirect('empresas:lista_empresas')
    
    # If GET request, show confirmation (though we'll use JavaScript confirmation)
    return redirect('empresas:lista_empresas')