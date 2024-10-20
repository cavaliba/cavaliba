# app_home - admin.py

from django.contrib import admin

from app_home.models import DashboardApp

# -----------------------------------
# DashboardApp
# ----------------------------------
#admin.site.register(DashboardApp)

@admin.register(DashboardApp)
class DashboardAppAdmin(admin.ModelAdmin):
    list_display = ('keyname','displayname','state', 'icon', 'url', 'order','version', 'id')
    ordering=['order']
    list_filter = ("state","page")
#    search_fields = ['name', 'amount','status']
