from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique  instances
from datetime import date

from django.contrib.auth.models import User  # Utilizado al asignar un usuario a cada prestamo


class Articulo(models.Model):
    """
    Modelo que representa un articulo
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000, help_text='Ingrese una breve descripcion del articulo')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unica para este articulo")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        """
        String que representa el articulo
        """
        return self.nombre


    def get_absolute_url(self):
        """
        retorna la url para acceder a ver el detalle del articulo
        """
        return reverse('articulo-detalle', args=[str(self.id)])




class Prestamo_articulo(models.Model):

    """
    Modelo que representa un prestamo/solicitud de un articulo
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unica para este prestamo")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    articulo = models.ForeignKey('Articulo', on_delete=models.SET_NULL, null=True, blank=True)
    #blank=True porque el campo no es requerido en el formulario
    fecha_devolucion = models.DateField(null=True)
    fecha_inicio = models.DateField(null=True)

    #@property  allows to access the computed value of combined_name like an attribute
    @property
    def is_overdue(self):
       if self.due_back and date.today() > self.due_back:
           return True
       return False


    ESTADO_PRESTAMO = (
       ('p', 'Pendiente'),
       ('a', 'Aceptado'),
       ('r', 'Rechazado'),  # se nego el prestamo
       ('c', 'Caducado'),   # se excedio fecha maxima de devolucion
       ('t', 'Terminado'),   # se devolvio objeto antes de fecha maxima de devolucion
    )

    estado = models.CharField(max_length=1, choices=ESTADO_PRESTAMO, blank=True, default='p', help_text='Estado del prestamo')

    class Meta:
        ordering = ["fecha_devolucion"]


    def __str__(self):
        return '{0} ({1})'.format(self.id,self.articulo.nombre)

    def get_absolute_url(self):
        return reverse('prestamo-articulo-detalle', args=[str(self.id)])
