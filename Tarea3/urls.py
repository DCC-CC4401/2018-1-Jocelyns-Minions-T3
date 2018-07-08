"""Tarea3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from inventario_CEI import views


urlpatterns = [
    path('landingAdmin/', views.landingAdmin, name='landingAdmin'),
    path('landingAdminArtSpaces/', views.landingAdminArtSpaces, name='landingAdminArtSpaces'),
    path('landingAdminCalendar/', views.landingAdminCalendar, name='landingAdminCalendar'),
    path('', views.base, name='base'),
    path('base/',include('inventario_CEI.urls')),
    path('artProfile/',include('inventario_CEI.urls')),
    path('landingNat/',include('inventario_CEI.urls')),
    path('landingAdmin/', include('inventario_CEI.urls')),

    path('',include('inventario_CEI.urls')),

    path('admin/', admin.site.urls),
    #path('',views.landingAdminArtSpaces, name='landingAdminArtSpaces'),
    #url(r'^$', views.homepage, name="homepage"),
    #url(r'^admin/', admin.site.urls),
    #url(r'^landingAdminArtSpaces/$', views.landingAdminArtSpaces, name='landingAdminArtSpaces'),

]
