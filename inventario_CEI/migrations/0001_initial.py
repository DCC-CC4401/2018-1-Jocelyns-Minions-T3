# Generated by Django 2.0.3 on 2018-05-06 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(help_text='Ingrese una breve descripcion del articulo', max_length=1000)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='ID unica para este articulo', primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Prestamo_articulo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='ID unica para este prestamo', primary_key=True, serialize=False)),
                ('fecha_devolucion', models.DateField(null=True)),
                ('fecha_inicio', models.DateField(null=True)),
                ('estado', models.CharField(blank=True, choices=[('p', 'Pendiente'), ('a', 'Aceptado'), ('r', 'Rechazado'), ('c', 'Caducado'), ('t', 'Terminado')], default='p', help_text='Estado del prestamo', max_length=1)),
                ('articulo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario_CEI.Articulo')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['fecha_devolucion'],
            },
        ),
    ]