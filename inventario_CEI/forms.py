from django import forms
from django.forms import ModelForm
from inventario_CEI import models

ESTADO_ARTICULO = (
       ('d', 'Disponible'),
       ('o', 'Ocupado'),
       ('rp','En reparacion'),
       ('p', 'Perdido'),
    )

class ReservaForm(ModelForm):
    class Meta:
        model=models.Prestamo_articulo
        fields = ['fecha_inicio','hora_inicio','fecha_devolucion','hora_devolucion']
        widgets = {
            'fecha_inicio': forms.SelectDateWidget(),
            'hora_inicio': forms.TimeInput(),
            'fecha_devolucion': forms.SelectDateWidget(),
            'hora_devolucion': forms.TimeInput(),
        }

class EditArticulo(ModelForm):
    class Meta:
        model=models.Articulo
        fields = ['nombre','descripcion','image','estado']
        labels = {
            'nombre':'Nombre',
            'descripcion': 'Descripción',
            'image': 'Imagen',
            'estado': 'estado',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.Textarea(attrs={'cols': 20, 'rows': 1}),
            'image':  forms.FileInput(),
            'estado': forms.Select(choices=ESTADO_ARTICULO),
        }
        help_texts ={
            'descripcion': None,
        }

class BorrarPrestamos(forms.Form):
    checkbox= forms.CheckboxInput()





