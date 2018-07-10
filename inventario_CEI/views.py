from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventario_CEI import models
from .forms import ReservaForm, EditArticulo, BorrarPrestamos
from .models import User, Articulo, Prestamo_articulo, Reserva_espacio


# Create your views here.
@login_required
def base(request):
    return render(request,'inventario_CEI/base.html')

@login_required
def artProfile(request,id):
    item = models.Articulo.objects.get(pk=id)
    prestamos = models.Prestamo_articulo.objects.filter(articulo=item)
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        form2 = EditArticulo(request.POST,request.FILES,instance=item)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.usuario=request.user
            instance.articulo=item
            instance.save()
            return redirect('/user')
        if form2.is_valid():
            instance=form2.save(commit=False)
            instance.save()
            return redirect(request.path_info)
        context = {'articulo': item, 'form': form, 'form2':form2,'prestamos': prestamos}
    else:
        form = ReservaForm()
        form2 = EditArticulo(instance=item)
        context = {'articulo': item, 'form': form, 'form2': form2, 'prestamos': prestamos}
    return render(request, 'inventario_CEI/artProfile.html',context)

@login_required
def usrProfile(request):
    if request.method == 'POST':
        if request.POST.getlist('check[]'):
            for id in request.POST.getlist('check[]'):
                item=models.Prestamo_articulo.objects.get(pk=id)
                item.delete()
        #models.Articulo.objects.filter(id__in=request.POST.getlist('checkbox')).delete()
        #return HttpResponse("hola")
    prestamos=models.Prestamo_articulo.objects.all().order_by('-fecha_hora_peticion')
    articulos=models.Articulo.objects.all()
    contexto={'prestamos':prestamos, 'articulos':articulos}
    return render(request, 'inventario_CEI/usrProfile.html',contexto)

def landingNatBase(request):
    return render(request, 'inventario_CEI/landing-nat-base.html')

def landingNatSearch(request):
    return render(request, 'inventario_CEI/landingNatSSearch.html')

def landingUserPlaceSearch(request):
    prestamos=models.Prestamo_articulo.objects.all()[0]
    context={'prestamos':prestamos}
    return render(request, 'inventario_CEI/landing-nat-place-search.html',context)

def landingAdminBase(request):
    return render(request, 'inventario_CEI/landingAdminBase.html')

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
    list_prestamos = Prestamo_articulo.objects.all().order_by('-fecha_hora_peticion')
    list_reserva =  Reserva_espacio.objects.all().order_by('-fecha_hora_peticion')
    latest = list(list_prestamos) + list(list_reserva)
    latest_sorted = sorted(latest, key=lambda x: x.fecha_hora_peticion, reverse=True)


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
                    if id.articulo.nombre:
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

