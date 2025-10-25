from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        # Si ya está autenticado y ya está en /login/, no redirigir para evitar bucle
        if request.path != reverse('dashboard:index'):
            return redirect(reverse('dashboard:index'))
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find user by email, then authenticate with username
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard:index'))
        else:
            messages.error(request, "Correo y/o contraseña incorrectos.")

    return render(request, 'login/login.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('login:home')  # Asegúrate que esta URL esté definida con name='index'

def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:index'))  # Adjust to your actual dashboard URL
    else:
        return render(request, 'login/home.html')  # This will display your home.html

from django.shortcuts import render

def password_reset_complete_custom(request):
    """
    Renderiza la página de 'contraseña restablecida con éxito'
    sin usar la implementación de Django que genera el error.
    """
    return render(request, 'login/password_reset_complete.html')
