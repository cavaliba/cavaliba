# app_conf - urls.py
# (c) cavaliba.com 


from django.urls import path

from app_conf import views

# url namespace
app_name="app_conf"

urlpatterns = [

    path('',  views.private, name='index'),

    # api
    #path('api/', views.api, name='api'),

    # anon
    #path('anon',  views.anonymous, name='anonymous'),


    # PRIVATE
    path('private/', views.private, name='private'),
    path('private/<slug:appname>/', views.private, name='private'),
    #path('private/list/', views.list, name='list'),
    #path('private/detail/<int:pageid>/', views.detail, name='detail'),


]