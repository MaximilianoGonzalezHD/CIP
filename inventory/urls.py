"""
URL configuration for CIP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import agregar_producto, agregar_material_usado, agregar_stock, crear_pedido, eliminar_producto, eliminar_solicitud, eliminar_usuario, inventario_gestion, login, home, logout, material, pedidos, productos_solicitados, registrar_usuario, gestion_usuarios, solicitud, solicitudes_archivadas, usar_material, ver_solicitud_archivada
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login, name='login'),
    path('home/', home, name='home'),
    path('registrar_usuario/', registrar_usuario, name='registrar_usuario'),
    path('inventario/', inventario_gestion, name='inventario'),
    path('gestion-usuarios/', gestion_usuarios, name='gestion-usuarios'),
    path('pedidos/', pedidos, name='pedidos'),
    path('material/', material, name='material'),
    path('solicitud/', solicitud, name='solicitud'),
     path('productos-solicitados/<int:solicitud_id>/', productos_solicitados, name='productos-solicitados'),
    path('agregar-producto/', agregar_producto, name='agregar-producto'),
    path('agregar-material-usado/<str:codigo>/', agregar_material_usado, name='agregar_material_usado'),
    path('logout/', logout, name='logout'),
    path('usuarios/eliminar/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('eliminar-producto/<str:codigo>/', eliminar_producto, name='eliminar_producto'),
    path('usar-material/<int:material_id>/', usar_material, name='usar_material'),
    path('agregar-stock/<str:codigo>/', agregar_stock, name='agregar_stock'),
    path('crear-pedido/', crear_pedido, name='crear_pedido'),
    path('eliminar-solicitud/<int:solicitud_id>/', eliminar_solicitud, name='eliminar_solicitud'),
    path('solicitudes-archivadas/', solicitudes_archivadas, name='solicitudes_archivadas'),
    path('solicitud_archivada/<int:solicitud_id>/', ver_solicitud_archivada, name='ver_solicitud_archivada'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
