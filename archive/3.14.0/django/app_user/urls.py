# app_user - urls.py
# (c) cavaliba.com 


from django.urls import path

from app_user import user_views
from app_user import group_views
from app_user import role_views
from app_user import ajax 


# url namespace
app_name="app_user"

urlpatterns = [

 
    # PRIVATE
    path('private/', user_views.private, name='private'),
    #path('private/list/', views.list, name='list'),
    #path('private/detail/<int:pageid>/', views.detail, name='detail'),
    path('private/debug/',  user_views.debug_env  , name='debug'),
    path('private/logout/', user_views.logout , name='logout'),

    # USER
    path('private/users/', user_views.list, name='user_list'),
    #path('private/users/import/', user_views.user_import, name='user_import'),
    path('private/user/detail/<int:userid>/', user_views.detail, name='user_detail'),
    path('private/user/detail/<str:login>/', user_views.detail, name='user_detail'),
    path('private/user/edit/', user_views.edit, name='user_edit'),
    path('private/user/edit/<int:userid>/', user_views.edit, name='user_edit'),
    path('private/user/edit/<str:login>/', user_views.edit, name='user_edit'),
    path('private/user/delete/<int:userid>/', user_views.delete, name='user_delete'),
    path('private/user/pref/', user_views.preferences, name='user_pref'),
    path('private/user/pref/<int:userid>/', user_views.preferences, name='user_pref'),
    path('private/user/email/test/<int:userid>/', user_views.email_test, name='email_test'),
    path('private/user/sms/test/<int:userid>/', user_views.sms_test, name='sms_test'),

    # groups
    path('private/groups/', group_views.list, name='group_list'),
    #path('private/groups/import/', group_views.group_import, name='group_import'),
    path('private/groups/edit/', group_views.edit, name='group_edit'),
    path('private/groups/edit/<int:gid>/', group_views.edit, name='group_edit'),
    path('private/groups/edit/<slug:keyname>/', group_views.edit, name='group_edit'),
    path('private/groups/detail/<int:gid>/', group_views.detail, name='group_detail'),
    path('private/groups/detail/<slug:gname>/', group_views.detail, name='group_detail'),
    path('private/groups/delete/<int:gid>/', group_views.delete, name='group_delete'),


    # roles
    path('private/roles/', role_views.list, name='role_list'),
    #path('private/roles/import/', role_views.role_import, name='role_import'),
    path('private/roles/edit/', role_views.edit, name='role_edit'),
    path('private/roles/edit/<int:gid>/', role_views.edit, name='role_edit'),
    path('private/roles/edit/<slug:keyname>/', role_views.edit, name='role_edit'),    
    path('private/roles/detail/<int:rid>/', role_views.detail, name='role_detail'),
    path('private/roles/detail/<slug:rname>/', role_views.detail, name='role_detail'),
    path('private/roles/delete/<int:gid>/', role_views.delete, name='role_delete'),

    # ajax 
    path('private/ajax/', ajax.ajax_user, name='ajax_user'),

    # api

]
