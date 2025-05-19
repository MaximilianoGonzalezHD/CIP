from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Rol, Usuario  # Asegúrate de que el modelo Usuario esté definido en models.py
from django.db import IntegrityError
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
# Create your views here.
#logueo
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_db = Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario no está registrado en el sistema.')
            return render(request, 'inventory/inicio/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'La contraseña es incorrecta.')
            return render(request, 'inventory/inicio/login.html')
    return render(request, 'inventory/inicio/login.html')

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), 'login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def home(request):
    return render(request, 'inventory/inicio/home.html')

#registro
def registrar_usuario(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        nombre_completo = request.POST.get('nombre_primero')
        apellido = request.POST.get('apellido')
        nombre_completo = f"{nombre_completo} {apellido}"
        correo = request.POST.get('correo')
        rut = request.POST.get('rut')
        rol_id = request.POST.get('rol')
        try:
            rol_instance = Rol.objects.get(pk=rol_id)
        except Rol.DoesNotExist:
            messages.error(request, 'El rol seleccionado no existe.')
            return render(request, 'inventory/inicio/registro.html')

        # Obtener los últimos 4 dígitos numéricos del RUT como contraseña
        rut_numeros = re.sub(r'\D', '', rut)  # Elimina todo lo que no sea dígito
        contrasena = rut_numeros[-4:] if len(rut_numeros) >= 4 else rut_numeros

        try:
            Usuario.objects.create_user(
            username=rut,
            password=contrasena,
            nombre_completo=nombre_completo,
            correo=correo,
            rut=rut,
            rol=rol_instance
            )
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('gestion-usuarios')
        except IntegrityError:
            messages.error(request, 'El nombre de usuario, correo o RUT ya existe.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar el usuario: {str(e)}')
    return render(request, 'inventory/inicio/registro.html')

@login_required_custom
def gestion_usuarios(request):
    return render(request, 'inventory/gestion/gestion-usuario.html')

#inventario
@login_required_custom
def inventario_gestion(request):
    return render(request, 'inventory/gestion/inventario.html')

@login_required_custom
def pedidos(request):
    return render(request, 'inventory/gestion/pedidos-proveedor.html')

@login_required_custom
def material(request):
    return render(request, 'inventory/gestion/material-usado.html')

@login_required_custom
def solicitud(request):
    return render(request, 'inventory/inicio/solicitudes-inventario.html')

@login_required_custom
def productos_solicitados(request):
    return render(request, 'inventory/gestion/productos-solicitados.html')

@login_required_custom
def agregar_producto(request):
    return render(request, 'inventory/gestion/agregar.html')

def logout(request):
    auth_logout(request)
    return redirect('login')