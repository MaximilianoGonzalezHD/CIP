from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Rol, Usuario, Reporte  # Asegúrate de que el modelo Usuario esté definido en models.py
from django.db import IntegrityError
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.utils import timezone
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
    fecha = request.GET.get('fecha', '')
    responsable_id = request.GET.get('responsable', '')

    reportes = Reporte.objects.all().order_by('-fecha', '-hora')

    if fecha:
        reportes = reportes.filter(fecha=fecha)
    if responsable_id:
        reportes = reportes.filter(usuario_id=responsable_id)

    # Para el filtro de responsables en el select
    responsables = Usuario.objects.filter(reporte__isnull=False).distinct()

    # Por defecto, muestra solo los últimos 20 si no hay filtros
    if not fecha and not responsable_id:
        reportes = reportes[:20]

    context = {
        'reportes': reportes,
        'responsables': responsables,
        'fecha': fecha,
        'responsable_id': responsable_id,
    }
    return render(request, 'inventory/inicio/home.html', context)

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
            nuevo_usuario = Usuario.objects.create_user(
                username=rut,
                password=contrasena,
                nombre_completo=nombre_completo,
                correo=correo,
                rut=rut,
                rol=rol_instance
            )
            Reporte.objects.create(
                usuario=request.user,
                descripcion=f"Se añadió a {nuevo_usuario.nombre_completo}, RUT: {nuevo_usuario.rut}, Cargo: {nuevo_usuario.rol}",
                fecha=timezone.now().date(),
                hora=timezone.now().time(),
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
    query = request.GET.get('q', '')
    usuarios = Usuario.objects.all()
    # Excluir superusuario (id=1 o is_superuser=True)
    usuarios = usuarios.exclude(is_superuser=True)
    if query:
        usuarios = usuarios.filter(
            Q(nombre_completo__icontains=query) |
            Q(rut__icontains=query) |
            Q(correo__icontains=query)
        )
    context = {
        'usuarios': usuarios
    }
    return render(request, 'inventory/gestion/gestion-usuario.html', context)

def eliminar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(pk=usuario_id)
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe.')
    return redirect('gestion-usuarios')

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