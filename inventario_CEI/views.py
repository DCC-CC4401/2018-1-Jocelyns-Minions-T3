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