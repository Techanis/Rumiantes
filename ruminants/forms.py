from django import forms
from .models import Ruminant, ModuloIoT

class RuminantForm(forms.ModelForm):
    # Explicitly define date fields to ensure proper handling
    fecha_ultimo_parto = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    fecha_servicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    fecha_esperada_parto = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Ruminant
        fields = [
            'empresa', 'modulo_iot', 'nombre', 'codigo', 'sexo', 'procedencia', 'padres', 
            'raza', 'categoria_reproductiva', 'categoria_productiva',
            'fecha_ultimo_parto', 'fecha_servicio', 'fecha_esperada_parto',
            'edad', 'dias_produccion', 'lactancia', 'estado_produccion', 'activo'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active companies
        self.fields['empresa'].queryset = self.fields['empresa'].queryset.filter(activo=True)
        # Only show active IoT modules
        self.fields['modulo_iot'].queryset = ModuloIoT.objects.filter(activo=True)
        
        # Set initial values for date fields in the correct format
        if self.instance and self.instance.pk:
            if self.instance.fecha_ultimo_parto:
                self.initial['fecha_ultimo_parto'] = self.instance.fecha_ultimo_parto
            if self.instance.fecha_servicio:
                self.initial['fecha_servicio'] = self.instance.fecha_servicio
            if self.instance.fecha_esperada_parto:
                self.initial['fecha_esperada_parto'] = self.instance.fecha_esperada_parto