from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PerfilUsuario, Empresa

class PerfilUsuarioForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(max_length=30, label="Nombre", required=True)
    last_name = forms.CharField(max_length=30, label="Apellido", required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Contraseña"
    )
    
    class Meta:
        model = PerfilUsuario
        fields = ['empresa', 'telefono', 'rol']  # Only profile fields
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        self.fields['empresa'].queryset = Empresa.objects.filter(activo=True)
        self.fields['rol'].choices = PerfilUsuario.ROL_CHOICES

        if self.request and not getattr(self.request.user.perfil, 'es_superadmin', False):
            self.fields['empresa'].required = False

        # 🔹 Restrict visible roles
        if self.request:
            current_role = getattr(self.request.user.perfil, 'rol', None)

            if current_role == 'admin':
                # Admin can create coadmins and users
                self.fields['rol'].choices = [
                    (r, label) for r, label in PerfilUsuario.ROL_CHOICES
                    if r in ('coadmin', 'jefe')
                ]
            elif current_role == 'coadmin':
                # Coadmin can only create normal users
                self.fields['rol'].choices = [
                    (r, label) for r, label in PerfilUsuario.ROL_CHOICES
                    if r == 'jefe'
                ]
        # If editing existing user, show their email/name
        if self.instance and self.instance.pk:
            self.fields['email'] = forms.EmailField(
                label="Email", 
                initial=self.instance.user.email,
                disabled=True  # Don't allow changing email when editing
            )
            self.fields['first_name'] = forms.CharField(
                max_length=30, 
                label="Nombre", 
                initial=self.instance.user.first_name
            )
            self.fields['last_name'] = forms.CharField(
                max_length=30, 
                label="Apellido", 
                initial=self.instance.user.last_name
            )
            self.fields['password'].required = False
            self.fields['password'].help_text = "Dejar vacío para mantener la contraseña actual"
    
    def clean_rol(self):
        rol = self.cleaned_data['rol']
        if self.request:
            current_role = self.request.user.perfil.rol

            if current_role == 'admin' and rol == 'superadmin':
                raise ValidationError("Los administradores no pueden crear superadministradores.")
            if current_role == 'coadmin' and rol != 'jefe':
                raise ValidationError("Los coadministradores solo pueden crear usuarios normales.")
        return rol

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        
        # Check if email already exists (for new users only)
        if not self.instance.pk and User.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está registrado.")
        
        return email
    
    def save(self, commit=True):
        # Get form data
        email = self.cleaned_data.get('email', '')
        first_name = self.cleaned_data.get('first_name', '')
        last_name = self.cleaned_data.get('last_name', '')
        password = self.cleaned_data.get('password', 'temp_password123')
        
        empresa = self.cleaned_data.get('empresa')
        if (not empresa) and self.request and not getattr(self.request.user.perfil, 'es_superadmin', False):
            empresa = self.request.user.perfil.empresa  # inject current admin's company

        if self.instance and self.instance.pk:
            # UPDATING EXISTING USER
            perfil = self.instance
            
            # Update user info
            perfil.user.first_name = first_name
            perfil.user.last_name = last_name
            if password:
                perfil.user.set_password(password)
            perfil.user.save()
            
            # Update profile
            perfil.empresa = self.cleaned_data['empresa']
            perfil.telefono = self.cleaned_data['telefono']
            perfil.rol = self.cleaned_data['rol']
            perfil.save()
            
            return perfil
        else:
            # CREATING NEW USER
            # 1. Create the User
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            
            # 2. Create the Profile
            perfil = PerfilUsuario.objects.create(
                user=user,
                empresa=empresa,
                #empresa=self.cleaned_data['empresa'],
                telefono=self.cleaned_data['telefono'],
                rol=self.cleaned_data['rol']
            )
            
            return perfil