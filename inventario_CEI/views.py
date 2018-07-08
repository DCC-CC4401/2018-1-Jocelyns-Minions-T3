from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
    return render(request, 'inventario_CEI/landingAdminUsers.html')

def landingAdminCalendar(request):
    return render(request, 'inventario_CEI/landingAdminCalendar.html')


def landingAdminArtSpaces(request):
    return render(request, 'inventario_CEI/landingAdminArtSpaces.html')
