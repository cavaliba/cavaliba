# app_data - urls.py
# (c) cavaliba.com 

from django.utils.translation import gettext as _
from django.urls import path

from app_data import views
from app_data import ajax 

# url namespace
app_name="app_data"

urlpatterns = [

    path('',  views.private, name='private'),

    # api
    #path('api/', views.api, name='api'),

    # anon
    #path('anon',  views.anonymous, name='anonymous'),


    # PRIVATE
    path('private/', views.private, name='private'),
    path('private/', views.private, name='class_list'),
    path('private/c/<slug:classname>/list/', views.instance_list, name='instance_list'),
    path('private/c/<slug:classname>/new/', views.instance_new, name='instance_new'),
    path('private/c/<slug:classname>/i/<slug:keyname>/detail/', views.instance_detail, name='instance_detail'),
    path('private/c/<slug:classname>/i/<slug:keyname>/edit/', views.instance_edit, name='instance_edit'),
    path('private/c/<slug:classname>/i/<slug:keyname>/delete/', views.instance_delete, name='instance_delete'),

    path('private/import/', views.data_import, name='data_import'),

    # ajax 
    path('private/ajax/', ajax.ajax_instance, name='ajax_instance'),

    #path('private/list/', views.list, name='list'),
    #path('private/detail/<int:pageid>/', views.detail, name='detail'),


]