from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import User, Articulo, Prestamo_articulo, Reserva_espacio


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

def landingAdminCalendar(request,caso="inventario_CEI/landingAdminCalendarTodos.html"):
    list_prestamos = Prestamo_articulo.objects.all().order_by('-fecha_inicio')
    list_reserva =  Reserva_espacio.objects.all().order_by('-fecha_inicio')
    latest = list(list_prestamos) + list(list_reserva)
    latest_sorted = sorted(latest, key=lambda x: x.fecha_inicio, reverse=True)


    return render(request,
                  caso,
                  context={'list_prestamos': list_prestamos, 'list_reserva': list_reserva, 'latest_sorted' :latest_sorted },
                  )


def modificarPendientes(request):
    if 'aceptar' in request.POST:
        if request.method == 'POST':
            if request.POST.getlist('check[]'):
                for id in request.POST.getlist('check[]'):
                    if item.articulo.nombre:
                        item = Prestamo_articulo.objects.get(pk=id)
                    else:
                        item = Reserva_espacio.objects.get(pk=id)

                    item.estado = "a"
                    item.save(update_fields=['estado'])



    elif 'rechazar' in request.POST:
        if request.method == 'POST':
            if request.POST.getlist('check[]'):
                for id in request.POST.getlist('check[]'):
                    if item.articulo.nombre:
                        item = Prestamo_articulo.objects.get(pk=id)
                    else:
                        item = Reserva_espacio.objects.get(pk=id)
                    item.estado = "r"
                    item.save(update_fields=['estado'])

    return landingAdminCalendar(request)


def modificarPedidos(request):

    if request.method == 'POST':
        if 'vigentes' in request.POST:
            return landingAdminCalendar(request, 'inventario_CEI/landingAdminCalendarVigentes.html')
        elif 'caducados' in request.POST:
            return landingAdminCalendar(request, 'inventario_CEI/landingAdminCalendarCaducados.html')
        elif 'todos' in request.POST:
            return landingAdminCalendar(request)
        elif 'perdidos' in request.POST:
            return landingAdminCalendar(request, 'inventario_CEI/landingAdminCalendarPerdidos.html')
        elif 'borrar' in request.POST:
            if request.POST.getlist('check[]'):
                for id in request.POST.getlist('check[]'):
                    if item.articulo.nombre:
                        item = Prestamo_articulo.objects.get(pk=id)
                    else:
                        item = Reserva_espacio.objects.get(pk=id)
                    item.delete()
                    return landingAdminCalendar(request)




    elif 'rechazar' in request.POST:
        if request.method == 'POST':
            if request.POST.getlist('check[]'):
                for id in request.POST.getlist('check[]'):
                    if item.articulo.nombre:
                        item = Prestamo_articulo.objects.get(pk=id)
                    else:
                        item = Reserva_espacio.objects.get(pk=id)
                    item.estado = "r"
                    item.save(update_fields=['estado'])




    #if 'list' in request.POST:
    # do some listing...
    #elif 'do-something-else' in request.POST:

    if request.method == 'POST':
        if request.POST.getlist('check[]'):
            for id in request.POST.getlist('check[]'):
                item=Prestamo_articulo.objects.get(pk=id)
                item.delete()
        #models.Articulo.objects.filter(id__in=request.POST.getlist('checkbox')).delete()

    #prestamos=Prestamo_articulo.objects.all().order_by('-fecha_hora_peticion')
    #articulos=models.Articulo.objects.all()
    #contexto={'prestamos':prestamos, 'articulos':articulos}
    #return render(request, 'inventario_CEI/usrProfile.html',contexto)

    return landingAdminCalendar(request)


def landingAdminArtSpaces(request):
    list_art = Articulo.objects.all() #articulos dup

    return render(
        request,
        'inventario_CEI/landingAdminArtSpaces.html',
        context={'list_art': list_art},
    )