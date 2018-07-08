from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns=[
    path('landingAdmin',views.landingAdmin,name='landingAdmin'),
    path('',views.base,name='base'),
    #path('',views.artProfile,name='artProfile'),
    #path('',views.usrProfile,name='usrProfile'),
    #path('',views.landingNat,name='landingNat'),

]