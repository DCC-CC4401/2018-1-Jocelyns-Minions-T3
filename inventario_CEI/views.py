from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventario_CEI import models
from .forms import ReservaForm, EditArticulo, BorrarPrestamos

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

def landingPlaceSearch(request):
    return render(request, 'inventario_CEI/landing-nat-place-search.html')

def landingAdminBase(request):
    return render(request, 'inventario_CEI/landingAdminBase.html')

def landingNat(request):
    return render(request,'inventario_CEI/landing-nat-advanced-search.html')

def landingAdmin(request):
    return render(request, 'inventario_CEI/landingAdminUsers.html')

def landingAdminCalendar(request):
    return render(request, 'inventario_CEI/landingAdminCalendar.html')

def landingAdminArtSpaces(request):
    return render(request, 'inventario_CEI/landingAdminArtSpaces.html')