# app_home - urls.py
# (c) cavaliba.com 


from django.urls import path, include

#from django.contrib import admin
#from django.shortcuts import render, redirect


#import app_home.views
from app_home import views

# url namespace
app_name="app_home"

urlpatterns = [

    # home/ >>  home/private/
    path('',  views.private, name='index'),
    path('private/', views.private, name='private'),

    # conf
    path('private/conf/', views.configuration, name='configuration'),
    path('private/conf/<slug:appname>/', views.configuration, name='configuration'),

    # logs
    path('private/log/', views.logview, name='log'),
    path('private/log/l/<str:level>/', views.logview, name='log'),
    path('private/log/purge/', views.logview, name='logpurge'),

]