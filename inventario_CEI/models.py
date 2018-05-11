from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique  instances
from datetime import date
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):

    def create_user(self, email, rut, nombres, apellidos, password=None):
        """
        Crea y guarda un User con el email, rut, nombres, apellidos y password dados.
        """
        if not email:
            raise ValueError('Los usuarios deben tener un e-mail')

        user = self.model(
            email=self.normalize_email(email),
            rut=rut,
            nombres=nombres,
            apellidos=apellidos,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, rut, nombres, apellidos, password):
        """
        Crea y guarda un SuperUser con el email, rut, nombres, apellidos y password dados.
        """
        user = self.create_user(
            email,
            rut=rut,
            nombres=nombres,
            apellidos=apellidos,
            password=password,
        )
        user.is_admin = True  # Esta es la unica diferencia entre un superusuario y un usuario normal.
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        primary_key=True,
    )
    rut = models.IntegerField(unique=True)
    '''
    Como tanto email y rut son unique (email es unique pues es primary key), no es necesario
    especificar un unique_together('rut','email').
    '''
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    puede_reservar = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut', 'nombres', 'apellidos']

    def get_nombre_simple(self):
        '''
        El nombre simple de un usuario es su primer nombre y su primer apellido.
        :return: Primer nombre seguido de primer apellido del usuario.
        '''
        return self.nombres.split(" ")[0]+" "+self.apellidos.split(" ")[0]

    def get_nombre_completo(self):
        '''
        En caso de que el usuario haya especificado solo un nombre y un apellido, este
        metodo es equivalente a get_nombre_simple.
        :return: Nombres seguido de los apellidos del usuario.
        '''
        return self.nombres+" "+self.apellidos

    def __str__(self):
        return self.get_nombre_simple()


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
