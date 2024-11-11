# app_home - admin.py

from django.contrib import admin

from app_home.models import DashboardApp
from app_home.models import CavalibaConfiguration

# -----------------------------------
# DashboardApp
# ----------------------------------
#admin.site.register(DashboardApp)

@admin.register(DashboardApp)
class DashboardAppAdmin(admin.ModelAdmin):
    list_display = ('keyname','displayname','is_enabled', 'page', 'order', 'icon', 'url', 'permission','id')
    ordering=['order']
    list_filter = ("is_enabled", "page")
#    search_fields = ['name', 'amount','status']






@admin.register(CavalibaConfiguration)
class CavalibaConfigurationAdmin(admin.ModelAdmin):
   list_display = ('appname', 'page','order', 'keyname','value','description','id')
   ordering=['appname', "page", "order"]
   list_filter = ["appname"]
#   search_fields = ['name', 'amount','status']

