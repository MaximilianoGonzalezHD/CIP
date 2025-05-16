from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Usuario  # Asegúrate de que el modelo Usuario esté definido en models.py

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

def home(request):
    return render(request, 'inventory/inicio/home.html')
#registro
def registrar_usuario(request):
    if request.method == 'POST':
        # Aquí luego procesaremos los datos
        pass
    return render(request, 'inventory/inicio/registro.html')

def gestion_usuarios(request):
    return render(request, 'inventory/gestion/gestion-usuario.html')

#inventario
def inventario_gestion(request):
    return render(request, 'inventory/gestion/inventario.html')

def pedidos(request):
    return render(request, 'inventory/gestion/pedidos-proveedor.html')

def material(request):
    return render(request, 'inventory/gestion/material-usado.html')

def solicitud(request):
    return render(request, 'inventory/inicio/solicitudes-inventario.html')

def productos_solicitados(request):
    return render(request, 'inventory/gestion/productos-solicitados.html')

def agregar_producto(request):
    return render(request, 'inventory/gestion/agregar.html')