from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = "login"
urlpatterns = [
    path('', views.home_redirect_view, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
# Rutas de recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='login/password_reset_form.html',
    email_template_name='login/reset_email.html',
    subject_template_name='login/reset_subject.txt',
    success_url=reverse_lazy('login:password_reset_done')
), name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='login/password_reset_confirm.html',
        success_url=reverse_lazy('login:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/',
        views.password_reset_complete_custom,
        name='password_reset_complete'),
]