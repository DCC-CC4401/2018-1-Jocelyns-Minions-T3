from django.urls import path

from . import views

urlpatterns=[
    #path('',views.base,name='base'),
    #path('',views.artProfile,name='artProfile'),
    #path('',views.usrProfile,name='usrProfile'),
    path('',views.landingNat,name='landingNat'),
]