from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from inventario_CEI.models import User, Articulo, Prestamo_articulo, Reserva_espacio, Espacio


class UserCreationForm(forms.ModelForm):
    '''
    Formulario para crear nuevos usuarios.
    Incluye todos los campos requeridos ademas de campos para contrasena y confirmacion de esta.
    '''
    password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contrasena', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'rut', 'nombres', 'apellidos', 'puede_reservar')

    def clean_password2(self):
        # Verificar que las contrasenas coincidan.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contrasenas no coinciden.")
        return password2

    def save(self, commit=True):
        # Guardar la contrasena.
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    '''
    Formulario para modificar usuarios.
    Incluye todos los campos requeridos.
    '''
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'rut', 'nombres', 'apellidos', 'puede_reservar', 'is_admin')

    def clean_password(self):
        # No entiendo bien que hace esto, pero es requerido por DjangoAdmin [Salu2 Gaspar] - oki doki [salu2 marcelo]
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # Los formularios para modificar y crear usuarios.
    form = UserChangeForm
    add_form = UserCreationForm

    # Los campos a mostrar para el modelo User.
    list_display = ('email', 'rut', 'nombres', 'apellidos', 'puede_reservar', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('rut', 'nombres', 'apellidos', 'puede_reservar',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'rut', 'nombres', 'apellidos', 'puede_reservar', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'rut',)
    ordering = ('rut',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Articulo)
admin.site.register(Prestamo_articulo)
admin.site.register(Reserva_espacio)
admin.site.register(Espacio)