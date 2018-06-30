from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def base(request):
    return render(request,'inventario_CEI/base.html')

def artProfile(request):
    return render(request, 'inventario_CEI/artProfile.html')

def usrProfile(request):
    return render(request, 'inventario_CEI/usrProfile.html')

def landingNat(request):
    return render(request,'inventario_CEI/landing-nat-advanced-search.html')

def landingAdmin(request):
    return render(request, 'inventario_CEI/landingAdminCalendar.html')