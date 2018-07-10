from django.urls import path
from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="inventario_CEI/login.html"), name='login'),
    path('base/', views.base, name='base'),
    path('articulos/<uuid:id>/', views.artProfile, name='artProfile'),
    path('user/', views.usrProfile, name='usrProfile'),
    path('landingAdmin/', views.landingAdmin, name='landingAdmin'),
    path('landingAdminArtSpaces/', views.landingAdminArtSpaces, name='landingAdminArtSpaces'),
    path('landingAdminCalendar/', views.landingAdminCalendar, name='landingAdminCalendar'),
    path('landingUser/',views.landingNat, name='landingUser'),
    path('landingUser/Asearch/',views.landingNatSearch, name='landingUser'),
    path('landingUserPlaceSearch/', views.landingUserPlaceSearch, name='UserPlaceSearch'),
    path('modificarPedidos', views.modificarPedidos, name='modificarPedidos'),
    path('modificarPendientes', views.modificarPendientes, name='modificarPendientes'),

]