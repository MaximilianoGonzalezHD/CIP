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
    imagen = models.ImageField(upload_to='inventory/images', null=True, blank=True)
    codigo = models.CharField(max_length=20, primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    metros = models.DecimalField(max_digits=10, decimal_places=2)
    ancho = models.DecimalField(max_digits=10, decimal_places=2)
    unidades_producto = models.IntegerField()
    altura = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    proveedor = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'rol__nombre': 'Proveedor'})
    bodega = models.ForeignKey('Bodega', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_producto

# Tabla de Material Utilizado
class MaterialUtilizado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_material = models.PositiveIntegerField(default=1)  # cuántos productos pasaste a material
    unidades_disponibles = models.PositiveIntegerField(default=0)  # ej: 7 clavos
    metros_disponibles = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ej: 8 metros
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.cantidad_material} material(es)"

# Tabla de Solicitudes de Pedido
class SolicitudPedido(models.Model):
    proveedor = models.ForeignKey(Usuario, related_name='solicitudes_proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    responsable = models.ForeignKey(Usuario, related_name='solicitudes_responsable', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)

class SolicitudArchivada(models.Model):
    proveedor = models.ForeignKey(Usuario, related_name='archivadas_proveedor', on_delete=models.SET_NULL, null=True, blank=True)
    responsable = models.ForeignKey(Usuario, related_name='archivadas_responsable', on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    fecha_archivado = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud archivada por {self.responsable} el {self.fecha_archivado}"
    
# Detalles de la solicitud (relación muchos-a-muchos)
class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(SolicitudPedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class DetalleSolicitudArchivada(models.Model):
    solicitud_archivada = models.ForeignKey('SolicitudArchivada', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"

# Reportes
class Reporte(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
