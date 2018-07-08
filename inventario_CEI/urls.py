from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('landingAdmin',views.landingAdmin,name='landingAdmin'),
    path('',views.base,name='base'),
    #path('',views.artProfile,name='artProfile'),
    #path('',views.usrProfile,name='usrProfile'),
    #path('',views.landingNat,name='landingNat'),
    path('login/', auth_views.LoginView.as_view(template_name="inventario_CEI/login.html"), name='login'),
    path('base/', views.base, name='base'),
    path('articulos/', views.artProfile, name='artProfile'),
    path('user/', views.usrProfile, name='usrProfile'),

]