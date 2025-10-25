from django.shortcuts import render
from ruminants.models import ModuloIoT,Ruminant,IoTData
from usuarios.decorators import mismo_empresa_required
from empresas.models import Empresa
# Create your views here.
@mismo_empresa_required
def dashboard_view(request):
    data = []
    empresa_usuario = request.user.perfil.empresa

    # Determine modules based on role
    if request.user.perfil.es_superadmin:
        modulos = ModuloIoT.objects.all()
        empresas = Empresa.objects.all()
        context = {
                'empresas': empresas
                    }
        return render(request, 'dashboard/dashboard_admin.html', context)
    else:
        modulos = ModuloIoT.objects.filter(empresa=empresa_usuario)

    # Loop through modules
    for modulo in modulos:
        # Get the ruminant linked to this IoT module
        ruminant = Ruminant.objects.filter(modulo_iot=modulo).first()

        # Get the latest 5 IoT data readings
        last_data = IoTData.objects.filter(modulo_iot=modulo).order_by('-timestamp').first()

        data.append({
            'modulo': modulo,
            'ruminant': ruminant,
            'iot_data': last_data,
        })

    context = {'data': data}
    return render(request, 'dashboard/dashboard.html', context)