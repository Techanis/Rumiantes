from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import usuario_required,admin_required,coadmin_required
from .models import Ruminant,ModuloIoT,IoTData
from .forms import RuminantForm

@usuario_required
def lista_ruminants(request):
    nameFilter = request.GET.get('name_query',"")
    estadoFilter = request.GET.get('estado_filter', "all" ) # Default to 'category'
    selectedView = request.GET.get('selected_View',"listview") 
    
    if request.user.perfil.es_superadmin:
        ruminants = Ruminant.objects.all()
    else:
        ruminants = Ruminant.objects.filter(empresa=request.user.perfil.empresa)
    ruminantsData = []    
    ruminantsLocation = []
    range_temp=[39.5,39]
    
    if nameFilter != "":
        ruminants = (ruminants.filter(nombre=nameFilter) or 
            ruminants.filter(codigo=nameFilter))
        
        
    for ruminant in ruminants:
        moduloIoT=ruminant.modulo_iot
        dataIoT= moduloIoT.iot_data.first()
         # 1=>crítico 2=precaución 3=>celo 4=>parto
        estado="active"
        if dataIoT.temperatura > range_temp[0]:
            estado="critical"
        elif dataIoT.temperatura > range_temp[1]:
            estado="caution"
        elif int(ruminant.categoria_reproductiva) == 3:
            estado="heat"             
        elif 0 :
            estado="delivery" 
        else :
            estado = "active"    
        ruminantsData.append((ruminant,dataIoT,estado))
        ruminantsLocation.append((dataIoT.latitud,dataIoT.longitud))
        
    if estadoFilter!= "all":
        ruminantsData = filter(lambda x: x[2]== estadoFilter, ruminantsData)
        
    
    context = {
        'ruminants': ruminants, 
        'ruminants_data': ruminantsData,
        'ruminants_location':  ruminantsLocation,
        'estado_filter' : estadoFilter,
        'selected_View':  selectedView 
    }
    
    if selectedView == "listview":
        return render(request, 'ruminants/lista_ruminants.html', context)
    else :
        return render(request, 'ruminants/lista_ruminants_map_square.html', context)

@coadmin_required
def agregar_ruminant(request):
    if request.method == 'POST':
        form = RuminantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ruminants:lista_ruminants')
    else:
        form = RuminantForm()
    
    context = {
        'form': form
    }
    return render(request, 'ruminants/agregar_ruminant.html', context)

@login_required
@admin_required
def editar_ruminant(request, ruminant_id):
    ruminant = get_object_or_404(Ruminant, id=ruminant_id)
    
    if request.method == 'POST':
        form = RuminantForm(request.POST, instance=ruminant)
        if form.is_valid():
            form.save()
            return redirect('ruminants:lista_ruminants')
    else:
        form = RuminantForm(instance=ruminant)
    
    context = {
        'form': form,
        'ruminant': ruminant
    }
    return render(request, 'ruminants/editar_ruminant.html', context)

@login_required
def eliminar_ruminant(request, ruminant_id):
    ruminant = get_object_or_404(Ruminant, id=ruminant_id)
    if request.method == 'POST':
        ruminant.delete()
    return redirect('ruminants:lista_ruminants')

@login_required
@usuario_required
def lista_iot_data(request):
    iot_data = IoTData.objects.all().order_by('-timestamp')
    
    # Filter by module if provided
    modulo_id = request.GET.get('modulo')
    if modulo_id:
        iot_data = iot_data.filter(modulo_iot_id=modulo_id)
    
    # Group by message timestamp to show related readings
    grouped_data = {}
    for data in iot_data:
        # Use the raw message timestamp to group related readings
        msg_timestamp = data.raw_data.get('timestamp', data.timestamp.isoformat())
        if msg_timestamp not in grouped_data:
            grouped_data[msg_timestamp] = []
        grouped_data[msg_timestamp].append(data)
    
    context = {
        'grouped_data': grouped_data,
        'modulos': ModuloIoT.objects.filter(activo=True)
    }
    return render(request, 'ruminants/lista_iot_data.html', context)

def lista_alerta(request):

    return render(request, 'ruminants/alertas.html')

def reporte(request):
    return render(request,'ruminants/reportes.html')