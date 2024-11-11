# app_home - urls.py
# (c) cavaliba.com 


from django.urls import path, include

#from django.contrib import admin
from django.shortcuts import render, redirect


#import app_home.views
from app_home import views

# url namespace
app_name="app_home"

urlpatterns = [

    # public
    path('',  views.private, name='index'),

    # api
    #path('api/',  views.api, name='api'),

    # anon
    #path('anon/',  views.anonymous, name='anonymous'),

    path('private/', views.private, name='private'),
    path('private/import/', views.yaml_import, name='yaml_import'),

    # conf
    path('private/conf/', views.configuration, name='configuration'),
    path('private/conf/<slug:appname>/', views.configuration, name='configuration'),
]