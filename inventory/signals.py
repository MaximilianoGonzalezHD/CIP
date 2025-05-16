from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Rol

User = get_user_model()

@receiver(post_save, sender=User)
def asignar_rol_admin(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        rol_admin, _ = Rol.objects.get_or_create(nombre='Administrador')
        instance.rol = rol_admin
        instance.save()