# {{ app_name }} - urls.py
# (c) cavaliba.com 

from django.utils.translation import gettext as _
from django.urls import path

from {{ app_name }} import views

# url namespace
app_name="{{ app_name }}"

urlpatterns = [

    path('',  views.index, name='index'),

    # api
    #path('api/', views.api, name='api'),

    # anon
    #path('anon',  views.anonymous, name='anonymous'),


    # PRIVATE
    path('private/', views.private, name='private'),
    #path('private/list/', views.list, name='list'),
    #path('private/detail/<int:pageid>/', views.detail, name='detail'),


]