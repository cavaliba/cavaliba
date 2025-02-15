# app_data - urls.py
# (c) cavaliba.com 

# from django.utils.translation import gettext as _
from django.urls import path

from app_data import views
from app_data import ajax 
from app_data import api

# url namespace
app_name="app_data"

urlpatterns = [

    path('',  views.private, name='private'),

    # api ; in descending order
    path('api/', api.index, name='api_index'),
    path('api/classes/', api.classes, name='api_classes'),
    path('api/c/<slug:classname>/', api.classname, name='api_classname'),
    path('api/c/<slug:classname>/i/<slug:keyname>/', api.instance, name='api_instance'),
    path('api/import/', api.api_import, name='api_import'),
    path('api/csv/<slug:classname>/', api.api_csv, name='api_csv'),

    # anon
    #path('anon',  views.anonymous, name='anonymous'),

    # PRIVATE
    path('private/', views.private, name='private'),
    path('private/', views.private, name='class_list'),
    path('private/c/<slug:classname>/list/', views.instance_list, name='instance_list'),
    path('private/c/<slug:classname>/new/', views.instance_new, name='instance_new'),
    path('private/c/<slug:classname>/i/<str:handle>/detail/', views.instance_detail, name='instance_detail'),
    path('private/c/<slug:classname>/i/<str:handle>/edit/', views.instance_edit, name='instance_edit'),
    path('private/c/<slug:classname>/i/<str:handle>/delete/', views.instance_delete, name='instance_delete'),

    #path('private/import/', views.data_import, name='data_import'),
    path('private/import/', views.data_import, name='data_import'),
    path('private/export/', views.data_export, name='data_export'),

    # ajax 
    path('private/ajax/', ajax.ajax_instance, name='ajax_instance'),

    #path('private/list/', views.list, name='list'),
    #path('private/detail/<int:pageid>/', views.detail, name='detail'),


]
