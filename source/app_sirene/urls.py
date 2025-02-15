 # (c) cavaliba.com - sirene - urls.py

from django.urls import path

from . import public_views
from . import anonymous_views
from . import category_views
from . import publicpage_views
from . import template_views
from . import message_views

from . import configuration_views
from . import api_views
from . import sms_views




# url namespace
app_name="app_sirene"

urlpatterns = [

    # PUBLIC
    path('', public_views.index, name='index'),
    #path('', views_public.index, name='public'),

    # Anonymous / Trusted IPs / No AUTH
    path('anon/index/',  anonymous_views.list, name='anonymous'),
    path('anon/detail/<int:pageid>/', anonymous_views.detail, name='anonymous_detail'),

    # API
    path('api/', api_views.index, name='api_index'),

    # MESSAGE & EDITOR
    path('private/',                          message_views.list, name='private'),
    path('private/history/',                  message_views.history, name='history'),
    path('private/detail/<int:pageid>/',      message_views.detail, name='detail'),
    path('private/update/<int:mid>/',         message_views.update, name='message_update'),
    path('private/remove/',                   message_views.remove, name='message_remove'),
    path('private/editor2/',                  message_views.editor2, name='message_editor'),
    path('private/editor2/<int:template_id>/', message_views.editor2, name='message_editor'),


    # Configuration & Tools
    #path('private/config/', configuration_views.config, name='config'),
    path('private/doc/',    configuration_views.doc    , name='doc'),
    # path('private/email_test/', configuration_views.email_test, name='email_test'),
    # path('private/email_test/<int:userid>/', configuration_views.email_test, name='email_test'),
    path('private/flushall/', configuration_views.flushall, name='flushall'),
    #path('private/import/', configuration_views.conf_import, name='conf_import'),
    path('private/export/', configuration_views.conf_export, name='conf_export'),

    # SMS
    path('private/sms/send/', sms_views.sms_send, name='sms_send'),
    path('private/sms/stat/', sms_views.sms_stat, name='sms_stat'),
    path('private/sms/journal/', sms_views.sms_journal, name='sms_journal'),

    # Template / Predefined
    path('private/template/', template_views.list, name='template_list'),
    path('private/template/edit/', template_views.edit, name='template_edit'),
    path('private/template/edit/<int:tid>/', template_views.edit, name='template_edit'),
    path('private/template/delete/<int:tid>/', template_views.delete, name='template_delete'),
    path('private/template/selector/', template_views.selector, name='template_selector'),

    # PUBLIC PAGES
    path('private/publicpage/', publicpage_views.list, name='publicpage_list'),
    path('private/config/publicpage/edit/', publicpage_views.edit, name='publicpage_edit'),
    path('private/config/publicpage/edit/<int:ppid>/', publicpage_views.edit, name='publicpage_edit'),
    path('private/config/publicpage/delete/<int:ppid>/', publicpage_views.delete, name='publicpage_delete'),
    #
    path('private/publicpage/selector/', publicpage_views.selector, name='publicpage_selector'),
    path('private/publicpage/preview/<int:ppid>/', publicpage_views.preview, name='publicpage_preview'),
    path('private/publicpage/push/<int:ppid>/', publicpage_views.push, name='publicpage_push'),
#    path('private/publicpage/reset/', publicpage_views.reset, name='public_reset'),



    # CATEGORY
    path('private/category/', category_views.list, name='category_list'),
    path('private/category/edit/', category_views.edit, name='category_edit'),
    path('private/category/edit/<int:cid>/', category_views.edit, name='category_edit'),
    path('private/category/delete/<int:cid>/', category_views.delete, name='category_delete'),


]
