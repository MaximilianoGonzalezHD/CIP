from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import DetalleSolicitudArchivada, Rol, SolicitudArchivada, Usuario, Reporte, Bodega, Producto, MaterialUtilizado, SolicitudPedido, DetalleSolicitud  # Asegúrate de que el modelo Usuario esté definido en models.py
from django.db import IntegrityError
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

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
    productos = Producto.objects.select_related('proveedor', 'bodega').all()
    if request.GET.get('q'):
        q = request.GET['q']
        productos = productos.filter(
            Q(nombre_producto__icontains=q) |
            Q(codigo__icontains=q) |
            Q(proveedor__nombre_completo__icontains=q)
        )
    return render(request, 'inventory/gestion/inventario.html', {'productos': productos})

@login_required_custom
def pedidos(request):
    if 'pedido' not in request.session:
        request.session['pedido'] = []

    if request.method == 'POST':
        print("POST recibido")  # <-- Esto debe aparecer en la consola
        codigo = request.POST.get('codigoProducto')
        cantidad = int(request.POST.get('cantidad', 0))
        try:
            producto = Producto.objects.get(codigo=codigo)
            pedido = request.session['pedido']
            for item in pedido:
                if item['codigo'] == codigo:
                    item['cantidad'] += cantidad
                    break
            else:
                pedido.append({
                    'codigo': producto.codigo,
                    'descripcion': producto.nombre_producto,
                    'cantidad': cantidad
                })
            request.session['pedido'] = pedido
            request.session.modified = True
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe.")

    if request.GET.get('eliminar'):
        codigo = request.GET.get('eliminar')
        pedido = request.session.get('pedido', [])
        pedido = [item for item in pedido if item['codigo'] != codigo]
        request.session['pedido'] = pedido
        request.session.modified = True
        return redirect('pedidos')

    productos = request.session.get('pedido', [])
    return render(request, 'inventory/gestion/pedidos-proveedor.html', {'productos': productos})

@login_required_custom
def material(request):
    materiales = MaterialUtilizado.objects.select_related('producto').all()
    productos = Producto.objects.all()
    return render(request, 'inventory/gestion/material-usado.html', {
        'materiales': materiales,
        'productos': productos
    })

@login_required_custom
def solicitud(request):
    solicitudes = SolicitudPedido.objects.select_related('proveedor').order_by('-fecha')
    return render(request, 'inventory/inicio/solicitudes-inventario.html', {'solicitudes': solicitudes})

@login_required_custom
def productos_solicitados(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudPedido, id=solicitud_id)
    detalles = DetalleSolicitud.objects.filter(solicitud=solicitud).select_related('producto')
    return render(
        request,
        'inventory/gestion/productos-solicitados.html',
        {
            'solicitud': solicitud,
            'detalles': detalles,
        }
    )

@login_required_custom
def agregar_producto(request):
    bodegas = Bodega.objects.all()
    proveedores = Usuario.objects.filter(rol__nombre="Proveedor")
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        metros = request.POST.get('metros')
        ancho = request.POST.get('ancho')
        altura = request.POST.get('altura')
        cantidad = request.POST.get('cantidad')
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        bodega_id = request.POST.get('bodega')
        unidades_producto = request.POST.get('unidades_producto')
        proveedor_id = request.POST.get('proveedor')
        imagen = request.FILES.get('imagen')

        # Validación básica
        if not (nombre and metros and ancho and altura and cantidad and codigo and descripcion and bodega_id and unidades_producto):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'inventory/gestion/agregar.html', {'bodegas': bodegas, 'proveedores': proveedores})

        try:
            bodega = Bodega.objects.get(id=bodega_id)
        except Bodega.DoesNotExist:
            messages.error(request, "La bodega seleccionada no existe.")
            return render(request, 'inventory/gestion/agregar.html', {'bodegas': bodegas, 'proveedores': proveedores})

        proveedor = None
        if proveedor_id:
            try:
                proveedor = Usuario.objects.get(id=proveedor_id)
            except Usuario.DoesNotExist:
                messages.error(request, "El proveedor seleccionado no existe.")
                return render(request, 'inventory/gestion/agregar.html', {'bodegas': bodegas, 'proveedores': proveedores})

        # Crear el producto
        try:
            producto = Producto.objects.create(
                codigo=codigo,
                nombre_producto=nombre,
                metros=metros,
                ancho=ancho,
                altura=altura,
                cantidad=cantidad,
                descripcion=descripcion,
                bodega=bodega,
                unidades_producto=unidades_producto,
                imagen=imagen,
                proveedor=proveedor
            )
            # Crear el reporte del movimiento
            Reporte.objects.create(
                usuario=request.user,
                descripcion=f"Se añadió el producto: {producto.nombre_producto}, Código: {producto.codigo}, Proveedor: {producto.proveedor.nombre_completo if producto.proveedor else 'Sin proveedor'}, Bodega: {producto.bodega.nombre if producto.bodega else 'Sin ubicación'}",
                fecha=timezone.now().date(),
                hora=timezone.now().time(),
            )
            messages.success(request, "Producto añadido correctamente.")
            return redirect('inventario')
        except Exception as e:
            messages.error(request, f"Error al añadir el producto: {str(e)}")

    return render(request, 'inventory/gestion/agregar.html', {'bodegas': bodegas, 'proveedores': proveedores})

@login_required_custom
def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
    return redirect('inventario')

@login_required_custom
def agregar_material_usado(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'POST':
        if producto.cantidad > 0:
            producto.cantidad -= 1
            producto.save()
            MaterialUtilizado.objects.create(
                producto=producto,
                cantidad_material=1,
                unidades_disponibles=producto.unidades_producto,
                metros_disponibles=producto.metros,
                usuario=request.user
            )
            # Reporte: Saco x producto del inventario
            Reporte.objects.create(
                usuario=request.user,
                descripcion=f"Sacó {producto.nombre_producto} del inventario para usarlo como material.",
                fecha=timezone.now().date(),
                hora=timezone.now().time(),
            )
            # NUEVO: Reporte si el producto queda sin stock
            if producto.cantidad == 0:
                usuario_sistema = Usuario.objects.filter(username='sistema').first()
                Reporte.objects.create(
                    usuario=usuario_sistema,
                    descripcion=f"{producto.nombre_producto} se ha quedado sin stock.",
                    fecha=timezone.now().date(),
                    hora=timezone.now().time(),
                )
            messages.success(request, "Material añadido correctamente.")
        else:
            messages.error(request, "No hay stock disponible para este producto.")
        return redirect('material')
    return redirect('material')

@csrf_exempt
@login_required_custom
def usar_material(request, material_id):
    material = get_object_or_404(MaterialUtilizado, id=material_id)
    unidades_usar = int(request.POST.get('usar_unidades', 0) or 0)
    metros_usar = request.POST.get('usar_metros', 0) or 0
    try:
        metros_usar = Decimal(metros_usar)
    except:
        metros_usar = Decimal(0)
    changed = False
    descripcion_reporte = ""

    if unidades_usar > 0 and material.unidades_disponibles >= unidades_usar:
        material.unidades_disponibles -= unidades_usar
        changed = True
        descripcion_reporte += f"Se usó {unidades_usar} unidad(es) de '{material.producto.nombre_producto}'. "

    if metros_usar > 0 and material.metros_disponibles >= metros_usar:
        material.metros_disponibles -= metros_usar
        changed = True
        descripcion_reporte += f"Se usó {metros_usar} metros de '{material.producto.nombre_producto}'. "

    if changed:
        # Si ambos llegan a 0, elimina el material utilizado
        if material.unidades_disponibles <= 0 and material.metros_disponibles <= 0:
            material.delete()
        else:
            material.save()
        # Crear el reporte solo si se usó algo
        Reporte.objects.create(
            usuario=request.user,
            descripcion=descripcion_reporte.strip(),
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
        )
    return redirect('material')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required_custom
def agregar_stock(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        if cantidad > 0:
            producto.cantidad += cantidad
            producto.save()
            messages.success(request, f"Se añadieron {cantidad} unidades al stock.")
        else:
            messages.error(request, "Cantidad inválida.")
    return redirect('inventario')

@login_required_custom
def crear_pedido(request):
    if request.method == 'POST':
        pedido = request.session.get('pedido', [])
        if not pedido:
            messages.error(request, "No hay productos en el pedido.")
            return redirect('pedidos')
        proveedor = Usuario.objects.filter(rol__nombre='Proveedor').first()
        solicitud = SolicitudPedido.objects.create(
            proveedor=proveedor,
            responsable=request.user
        )
        for item in pedido:
            producto = Producto.objects.get(codigo=item['codigo'])
            DetalleSolicitud.objects.create(
                solicitud=solicitud,
                producto=producto,
                cantidad=item['cantidad']
            )
        # --- REPORTE ---
        Reporte.objects.create(
            usuario=request.user,
            descripcion=f"Se ha creado un pedido (ID: {solicitud.id}).",
            fecha=timezone.now().date(),
            hora=timezone.now().time(),
        )
        request.session['pedido'] = []
        messages.success(request, "Pedido creado correctamente.")
        return redirect('pedidos')
    return redirect('pedidos')

@login_required_custom
def solicitudes_archivadas(request):
    solicitudes = SolicitudArchivada.objects.all()
    return render(request, 'inventory/inicio/solicitudes_archivadas.html', {'solicitudes': solicitudes})

@login_required_custom
def ver_solicitud_archivada(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArchivada, id=solicitud_id)
    detalles = solicitud.detalles.all()  # gracias al related_name='detalles'
    return render(request, 'inventory/gestion/detalles_solicitudes.html', {
        'solicitud': solicitud,
        'detalles': detalles
    })

@login_required_custom
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudPedido, id=solicitud_id)

    # 1. Crear la solicitud archivada
    solicitud_archivada = SolicitudArchivada.objects.create(
        proveedor=solicitud.proveedor,
        responsable=solicitud.responsable,
        fecha=solicitud.fecha
    )

    # 2. Traspasar los detalles a DetalleSolicitudArchivada
    detalles = DetalleSolicitud.objects.filter(solicitud=solicitud)
    for detalle in detalles:
        DetalleSolicitudArchivada.objects.create(
            solicitud_archivada=solicitud_archivada,
            producto=detalle.producto,
            cantidad=detalle.cantidad
        )

    solicitud.delete()

    # 3. Reporte
    Reporte.objects.create(
        usuario=request.user,
        descripcion=f"Solicitud archivada (ID: {solicitud_id}) con todos sus productos.",
        fecha=timezone.now().date(),
        hora=timezone.now().time(),
    )

    messages.success(request, "Solicitud archivada correctamente.")
    return redirect('solicitud')