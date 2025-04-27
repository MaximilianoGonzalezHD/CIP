from django.shortcuts import render

# Create your views here.
#logueo
def login(request):
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

