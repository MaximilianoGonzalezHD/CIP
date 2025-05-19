from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    # Campos adicionales
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rut = models.CharField(max_length=15, unique=True, null=True, blank=True)
    contrasena = models.CharField(max_length=128)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
# Tabla de Productos
class Producto(models.Model):
    imagen = models.ImageField(upload_to='static/inventory/images', null=True, blank=True)
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    metros = models.DecimalField(max_digits=10, decimal_places=2)
    ancho = models.DecimalField(max_digits=10, decimal_places=2)
    altura = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_producto

# Tabla de Material Utilizado
class MaterialUtilizado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    metros_usados = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_uso = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

# Tabla de Solicitudes de Pedido
class SolicitudPedido(models.Model):
    proveedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol__nombre': 'Proveedor'})
    fecha = models.DateField(auto_now_add=True)

# Detalles de la solicitud (relación muchos-a-muchos)
class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudPedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

# Reportes
class Reporte(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)