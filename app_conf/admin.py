# app_conf - admin.py

from django.contrib import admin


from app_conf.models import SireneConfiguration


@admin.register(SireneConfiguration)
class SireneConfigurationAdmin(admin.ModelAdmin):
   list_display = ('appname', 'page','order', 'keyname','value','description','id')
   ordering=['appname', "page", "order"]
   list_filter = ["appname"]
#   search_fields = ['name', 'amount','status']
