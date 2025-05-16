from django.contrib import admin
from .models import Usuario, Rol
from django.contrib.auth.admin import UserAdmin

admin.site.register(Rol)
admin.site.register(Usuario, UserAdmin)
# Register your models here.
