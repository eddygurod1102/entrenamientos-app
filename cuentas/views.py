from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)

class VistaIniciarSesion(LoginView):
    template_name = 'cuentas/login.html'

class VistaCerrarSesion(LogoutView):
    pass

class VistaCambiarContraseña(PasswordChangeView):
    template_name = 'cuentas/formulario_cambiar_contraseña.html'

class VistaResetearContraseña(PasswordResetView):
    template_name = 'cuentas/formulario_resetear_contraseña.html'
    email_template_name = 'cuentas/resetear_contraseña_email.html'
    success_url = reverse_lazy('resetear_contrasena_hecho')

class VistaResetearContraseñaHecho(PasswordResetDoneView):
    template_name = 'cuentas/resetear_contraseña_hecho.html'

class VistaResetarContraseñaConfirmar(PasswordResetConfirmView):
    pass