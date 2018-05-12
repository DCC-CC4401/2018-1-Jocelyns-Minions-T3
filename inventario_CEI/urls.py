from django.urls import path

from . import views

urlpatterns=[
    path('base/',views.base,name='base'),
    path('articulos/',views.artProfile,name='artProfile'),
    path('user/',views.usrProfile,name='usrProfile'),
]