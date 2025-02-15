# (c) - cavaliba.com
# core urls.py

from django.urls import include, path
from django.shortcuts import render, redirect

import debug_toolbar

import app_sirene.public_views
import app_home.views

from django.contrib import admin

admin.site.site_header = 'CAVALIBA DB ADMIN'
admin.site.site_title = 'Cavaliba'
admin.site.site_name = "Cavaliba Admin Tools"


urlpatterns = [

    # /status/   => app_home status
    path('status/', app_home.views.status, name='status'),

    # /  >> /sirene/
    path('', app_sirene.public_views.index),

    # home/  >> app_home
    path('home/', include('app_home.urls')),

    # sirene/
    path('sirene/', include('app_sirene.urls')),
#    path('', include('app_sirene.urls')),

    # user/
    path('user/', include('app_user.urls')),

    # data
    path('data/', include('app_data.urls')),

    # local django auth 
    path("accounts/", include("django.contrib.auth.urls")),

    # django admin
    path('private/admin/', admin.site.urls),
    path('private/tinymce/', include('tinymce.urls')),
    

    path("private/__debug__/", include("debug_toolbar.urls")),

    # Deprecated:  OKTA login Init URI
    #path('private/', lambda request: redirect('app_sirene:private', permanent=False)),


]

