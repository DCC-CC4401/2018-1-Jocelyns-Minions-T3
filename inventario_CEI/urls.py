from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="inventario_CEI/login.html"), name='login'),
    path('base/', views.base, name='base'),
    path('articulos/<uuid:id>/', views.artProfile, name='artProfile'),
    path('user/', views.usrProfile, name='usrProfile'),
    #path('landingBase/', views.landingNatBase, name='landingBase'),
    url(r'^home/$', views.landingHome, name="landingHome"),
    url(r'^home/results/$', views.Search, name="search"),
]