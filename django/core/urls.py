"""SIRENE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


from django.urls import include, path
from django.shortcuts import render, redirect

import debug_toolbar

#import app_home.views
import app_sirene.public_views


from django.contrib import admin

admin.site.site_header = 'SIRENE DB ADMIN'
admin.site.site_title = 'Sirene'
admin.site.site_name = "Sirene Admin Tools"



urlpatterns = [

    # /  - NEXT: /home/
    path('', app_sirene.public_views.index),


    # app_home
    path('home/', include('app_home.urls')),


    # app_sirene
    path('sirene/', include('app_sirene.urls')),
#    path('', include('app_sirene.urls')),

    # app_user
    path('user/', include('app_user.urls')),

    # app_data
    path('data/', include('app_data.urls')),

    # app_log
    path('log/', include('app_log.urls')),

    # local django auth 
    path("accounts/", include("django.contrib.auth.urls")),

    # django admin
    path('private/admin/', admin.site.urls),
    path('private/tinymce/', include('tinymce.urls')),
    

    path("private/__debug__/", include("debug_toolbar.urls")),

    # Deprecated:  OKTA login Init URI
    path('private/', lambda request: redirect('app_sirene:private', permanent=False)),


]

