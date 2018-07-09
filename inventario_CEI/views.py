from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import User, Articulo, Prestamo_articulo


# Create your views here.
@login_required
def base(request):
    return render(request,'inventario_CEI/base.html')

@login_required
def artProfile(request):
    return render(request, 'inventario_CEI/artProfile.html')

@login_required
def usrProfile(request):
    return render(request, 'inventario_CEI/usrProfile.html')

def landingNat(request):
    return render(request,'inventario_CEI/landing-nat-advanced-search.html')

def landingAdmin(request):
    list_users = User.objects.all()

    return render(
        request,
        'inventario_CEI/landingAdminUsers.html',
        context={'list_users': list_users},
    )
    #return render(request, 'inventario_CEI/landingAdminUsers.html')

def landingAdminCalendar(request):
    list_prestamos = Prestamo_articulo.objects.all() #duplicar
    return render(request,
                  'inventario_CEI/landingAdminCalendar.html',
                  context={'list_prestamos': list_prestamos},
                  )


def landingAdminArtSpaces(request):
    list_art = Articulo.objects.all() #articulos dup

    return render(
        request,
        'inventario_CEI/landingAdminArtSpaces.html',
        context={'list_art': list_art},
    )