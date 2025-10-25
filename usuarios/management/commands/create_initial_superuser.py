from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario, Empresa
import os

class Command(BaseCommand):
    """Safe command that can be run multiple times in production"""
    
    def handle(self, *args, **options):
        email = os.getenv('SUPERUSER_EMAIL', 'admin@empresa.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'changeme123')
        
        # Ensure company exists
        empresa, _ = Empresa.objects.get_or_create(
            nombre="Empresa Principal",
            defaults={
                'ruc': '00000000000',
                'email': 'admin@empresa.com',
                'activo': True
            }
        )
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'is_superuser': True,
                'is_staff': True,
                'first_name': 'Super',
                'last_name': 'Admin'
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f'Created superuser: {email}')
        else:
            # Ensure existing user is superuser
            if not user.is_superuser:
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                user.save()
                self.stdout.write(f'Updated user to superuser: {email}')
        
        # Profile will be created by signal automatically
        # But let's ensure it has the right role
        if hasattr(user, 'perfil'):
            if user.perfil.rol != 'superadmin':
                user.perfil.rol = 'superadmin'
                user.perfil.save()
                self.stdout.write(f'Updated profile role for: {email}')
        else:
            self.stdout.write(f'Profile will be created by signal for: {email}')
        
        self.stdout.write(self.style.SUCCESS('Superuser setup completed'))