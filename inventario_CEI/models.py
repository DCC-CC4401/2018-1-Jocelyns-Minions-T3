from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique  instances
from datetime import date
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.exceptions import ValidationError
from datetime import datetime

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
        verbose_name='Correo Electrónico',
        max_length=255,
        primary_key=True,
    )
    rut = models.IntegerField(unique=True, verbose_name="RUT")
    '''
    Como tanto email y rut son unique (email es unique pues es primary key), no es necesario
    especificar un unique_together('rut','email').
    '''
    nombres = models.CharField(max_length=200, verbose_name="Nombres")
    apellidos = models.CharField(max_length=200, verbose_name="Apellidos")
    puede_reservar = models.BooleanField(default=True, verbose_name="Habilitado para Reservar")
    is_admin = models.BooleanField(default=False, verbose_name="Es Administrador")

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

    def get_digito_verificador(self):
        '''
        Calcula y retorna el digito verificador del RUT del usuario.
        :return: Digito verificador de RUT del usuario.
        '''
        rut = int(self.rut)
        s = 0
        f = 2
        while rut != 0:
            digito = int(rut % 10)
            rut = int(rut / 10)
            s += f * digito
            if f == 7:
                f = 2
            else:
                f += 1

        dv_raw = 11 - (s % 11)
        if dv_raw == 11:
            return 0
        elif dv_raw == 10:
            return 'K'
        else:
            return dv_raw

    def __str__(self):
        return self.get_nombre_simple()

    @property
    def get_permiso(self):
        return self.puede_reservar

    def has_perm(self, perm, obj=None):
        '''
        Requerido para poder usar este modelo en Django Admin.
        Verifica si el usario posee el permiso <perm>.
        :param perm: Permiso a testear.
        :param obj:
        :return: Retorna True si el usuario tiene el permiso.
        '''
        return True

    def has_module_perms(self, app_label):
        '''
        Requerido para poder usar este modelo en Django Admin.
        :param app_label: Nombre de la aplicacion para la que se testean los permisos.
        :return: Retorna True si el usuario tiene permisos para ver la aplicacion <app_label>.
        '''
        return True

    @property
    def is_staff(self):
        '''
        Requerido para poder usar este modelo en Django Admin.
        :return: Retorna True si es super usuario (i.e si is_admin==True)
        '''
        return self.is_admin


class Articulo(models.Model):
    """
    Modelo que representa un articulo
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000, help_text='Ingrese una breve descripcion del articulo')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unica para este articulo")
    image = models.ImageField(upload_to='templates/media/', blank=True)
    ESTADO_ARTICULO = (
       ('d', 'Disponible'),
       ('o', 'Ocupado'),
       ('rp','En reparacion'),
       ('p', 'Perdido'),

    )
    estado = models.CharField(max_length=1, choices=ESTADO_ARTICULO, blank=True, default='d', help_text='Estado del articulo')

    ESTADO_ARTICULO = (
       ('d', 'Disponible'),
       ('e', 'En Prestamo'),
       ('p', 'Perdido'),  # se nego el prestamo
    )

    estado = models.CharField(max_length=1, choices=ESTADO_ARTICULO, blank=True, default='d', help_text='Estado del prestamo')



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

class Espacio(models.Model):
    """
    Modelo que representa un articulo
    """
    nombre = models.CharField(max_length=200)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unica para este espacio")

    ESTADO_ESPACIO = (
       ('d', 'Disponible'),
       ('e', 'En Prestamo'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_ESPACIO, blank=True, default='d', help_text='Estado del prestamo')



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

    @property
    def get_estado(self):
        dictionary = dict(self.ESTADO_ARTICULO)
        return dictionary[self.estado]




class Prestamo_articulo(models.Model):

    """
    Modelo que representa un prestamo/solicitud de un articulo
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unica para este prestamo")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #blank=True porque el campo no es requerido en el formulario
    fecha_inicio = models.DateField(null=True)
    hora_inicio = models.TimeField(null=True)
    fecha_devolucion = models.DateField(null=True)
    hora_devolucion = models.TimeField(null=True)
    fecha_hora_peticion= models.DateTimeField(auto_now=True)
    articulo = models.ForeignKey('Articulo', on_delete=models.SET_NULL, null=True, blank=True)
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
        ordering = ["fecha_hora_peticion"]

    @property
    def get_estado(self):
        dictionary= dict(self.ESTADO_PRESTAMO)
        return dictionary[self.estado]

    @property
    def get_name_articulo(self):
        return str(self.articulo)

    def __str__(self):
        return '{0} ({1})'.format(self.id,self.articulo.nombre)

    def get_absolute_url(self):
        return reverse('prestamo-articulo-detalle', args=[str(self.id)])


    @staticmethod
    def borrar():
        try:
            item = Prestamo_articulo.objects.get(pk=id)
        except Prestamo_articulo.DoesNotExist:
            return
        if item.estado=='p':
            item.delete()

    def save(self, *args, **kwargs):
        #MINIMO DE UNA HORA PARA RESERVAR
        if   (self.hora_inicio-self.fecha_hora_peticion)<1 :
            raise ValidationError
        else:
            super(Reserva_espacio, self).save(*args, **kwargs)




class Reserva_espacio(models.Model):

    """
    Modelo que representa un prestamo/solicitud de un articulo
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="ID unica para esta reserva")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    espacio = models.ForeignKey('Espacio', on_delete=models.SET_NULL, null=True, blank=True)
    #blank=True porque el campo no es requerido en el formulario
    fecha_inicio = models.DateField(null=True)
    hora_inicio = models.TimeField(null=True)
    fecha_devolucion = models.DateField(null=True)
    hora_devolucion = models.TimeField(null=True)
    fecha_hora_peticion = models.DateTimeField(auto_now=True)


    ESTADO_RESERVA = (
       ('p', 'Pendiente'),
       ('a', 'Aceptado'),
       ('r', 'Rechazado'),  # se nego el prestamo
    )

    estado = models.CharField(max_length=1, choices=ESTADO_RESERVA, blank=True, default='p', help_text='Estado del prestamo')

    class Meta:
        ordering = ["fecha_devolucion"]


    def __str__(self):
        return '{0} ({1})'.format(self.id,self.espacio.nombre)

    def get_absolute_url(self):
        return reverse('reserva-espacio-detalle', args=[str(self.id)])

    def save(self, *args, **kwargs):
        #MINIMO DE HORAS PARA RESERVAR
        fecha_hora_inicio= datetime.combine(self.fecha_inicio, self.hora_inicio)
        # MINIMO DE UNA HORA PARA RESERVAR
       git chec

        if False: #ver delta menor a una hora
            raise ValidationError
        else:
            super(Reserva_espacio, self).save(*args, **kwargs)




