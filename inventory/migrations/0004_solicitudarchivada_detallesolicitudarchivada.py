# Generated by Django 5.2.1 on 2025-06-03 08:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_solicitudpedido_responsable_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudArchivada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('fecha_archivado', models.DateField(auto_now_add=True)),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archivadas_proveedor', to=settings.AUTH_USER_MODEL)),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='archivadas_responsable', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleSolicitudArchivada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.producto')),
                ('solicitud_archivada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='inventory.solicitudarchivada')),
            ],
        ),
    ]
