from django.urls import path, include
from django.contrib.auth.views import LoginView, PasswordChangeView
from .views import (
    VistaIniciarSesion,
    VistaCerrarSesion,
    VistaCambiarContraseña,
    VistaResetearContraseña,
    VistaResetearContraseñaHecho,
    VistaAgregarUsuario,
)

urlpatterns = [
    path('login/', VistaIniciarSesion.as_view(), name='login'),
    path('logout/', VistaCerrarSesion.as_view(), name='logout'),
    path('cambiar_contraseña/', VistaCambiarContraseña.as_view(), name='cambiar_contrasena'),
    path('resetear_contraseña/', VistaResetearContraseña.as_view(), name='resetear_contrasena'),
    path('resetear_contraseña/hecho/', VistaResetearContraseñaHecho.as_view(), name='resetear_contrasena_hecho'),
    path('crear_usuario/', VistaAgregarUsuario.as_view(), name='crear_usuario'),
]