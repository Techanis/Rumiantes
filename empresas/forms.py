from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'ruc', 'telefono', 'email', 'direccion']

            # Custom validations Aquíse pueden agregar validaciones extra
    # def clean_nombre(self):
    #     nombre = self.cleaned_data['nombre']
    #     if len(nombre) < 3:
    #         raise forms.ValidationError("El nombre debe tener al menos 3 caracteres")
    #     return nombre