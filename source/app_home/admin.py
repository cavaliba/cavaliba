# (c) cavaliba.com - home - admin.py

from django.contrib import admin

from app_home.models import DashboardApp
from app_home.models import CavalibaConfiguration
from app_home.models import CavalibaLog
from app_home.models import CavalibaAPIStat

# -----------------------------------
# DashboardApp
# ----------------------------------
#admin.site.register(DashboardApp)

@admin.register(DashboardApp)
class DashboardAppAdmin(admin.ModelAdmin):
    list_display = ('keyname','displayname','is_enabled', 'sidebar_section','dashboard_section', 'order', 'icon', 'url', 'permission','id')
    ordering=['order']
    list_filter = ("is_enabled", "sidebar_section","dashboard_section")
#    search_fields = ['name', 'amount','status']


@admin.register(CavalibaConfiguration)
class CavalibaConfigurationAdmin(admin.ModelAdmin):
   list_display = ('appname', 'page','order', 'keyname','value','description','id')
   ordering=['appname', "page", "order"]
   list_filter = ["appname"]
#   search_fields = ['name', 'amount','status']



@admin.register(CavalibaLog)
class CavalibaLogAdmin(admin.ModelAdmin):
    list_display = ('created','username', 'user_ip', 'level','app','view','action','status', 'data')
    ordering=['created']
    list_filter = ["app","status"]
    #search_fields = ['name', 'amount','status']


@admin.register(CavalibaAPIStat)
class CavalibaAPIStatAdmin(admin.ModelAdmin):
    list_display = ('keyname','last_success', 'success_count', 'last_error','error_count')
    ordering=['keyname']
    # list_filter = ["app","status"]
    #search_fields = ['name', 'amount','status']