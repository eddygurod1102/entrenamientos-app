# Validadores para formularios (Por alguna extraña razón, no funcionan el RegexValidator
# que ofrece Django jajaj. Si vuelve a funcionar, dejaré de usar estos validadores).
from django.forms import ValidationError
from django.contrib.auth.models import User
import re

def validar_nombre(nombre):
    expresion = '^[A-Z][a-z]+$'

    if re.match(expresion, nombre) is None:
        raise ValidationError('Formato de nombre incorrecto.')

def validar_apellido(apellido):
    expresion = '^[A-Z][a-z]+$'

    if re.match(expresion, apellido) is None:
        raise ValidationError('Formato de apellido incorrecto.')

def validar_edad(edad):
    expresion = '\d{1,2}'

    if re.match(expresion, edad) is None:
        raise ValidationError('Formato de edad incorrecto.')

def validar_fotografia(fotografia):
    expresion = '^[\w\d\-\_]+\.(jpeg|jpg|png)$'

    if re.match(expresion, fotografia) is None:
        print(fotografia)
        raise ValidationError('Formato de fotografía incorrecto.')
    
def validar_nombre_usuario(nombre_usuario):
    expresion = '^[(A-Z)?a-z(\d+)?(\-+\_+)?]+$'

    if re.match(expresion, nombre_usuario) is None:
        raise ValidationError('Nombre de usuario no válido.')
    else:
        if User.objects.filter(username = nombre_usuario).count() == 1:
            raise ValidationError('Este nombre de usuario ya existe.')
        
def validar_correo_electronico(correo):
    expresion = '^[A-Za-z0-9\.\-\_]+\@([a-z]+\.?)+\.[a-z]+$'

    if re.match(expresion, correo) is None:
        raise ValidationError('Inserte un correo electrónico válido.')
    else:
        if User.objects.filter(email = correo).count() == 1:
            raise ValidationError('Ya existe un usuario que utiliza este correo electrónico.')

def validar_contrasena(contrasena):
    expresion = '^[A-Za-z0-9\.\-\_\!]{8,}$'

    if re.match(expresion, contrasena) is None:
        raise ValidationError('Cotraseña débil o no cumple con el requerimiento.')