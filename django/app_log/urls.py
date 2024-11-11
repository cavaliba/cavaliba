# app_log - urls.py
# (c) cavaliba.com 


from django.urls import path

from app_log import views

# url namespace
app_name="app_log"

urlpatterns = [

    path('',  views.private, name='index'),

    # api
    #path('api/', views.api, name='api'),

    # anon
    #path('anon',  views.anonymous, name='anonymous'),


    # PRIVATE
    path('private/', views.private, name='private'),
    path('private/l/<str:level>/', views.private, name='private'),
    path('private/purge/', views.private, name='log_purge'),

    #path('private/list/', views.list, name='list'),
    #path('private/detail/<int:pageid>/', views.detail, name='detail'),


]