# app_data - admin.py

from django.contrib import admin

# from app_data.models import DataStatic
# from app_data.models import DataStaticValue
from app_data.models import DataClass
from app_data.models import DataSchema
from app_data.models import DataInstance





# @admin.register(DataStatic)
# class DataStaticAdmin(admin.ModelAdmin):
#    list_display = ('keyname', 'displayname', 'is_enabled', 'id')
#    ordering=["keyname"]
#    # list_filter = ["appname"]
#    # search_fields = ['name', 'amount','status']


# @admin.register(DataStaticValue)
# class DataStaticValueAdmin(admin.ModelAdmin):
#    list_display = ('datastatic', 'value', 'order', 'is_enabled', 'id')
#    ordering=["datastatic","order"]
#    list_filter = ["datastatic"]


@admin.register(DataClass)
class DataClassAdmin(admin.ModelAdmin):
   list_display = ('keyname', 'displayname', 'is_bigset', 'count_estimation', 'order', 'page', 'is_enabled', 'id')
   ordering=["keyname"]
   list_filter = ["page"]
# @admin.register(DataClassPermission)
# class DataClassPermissionAdmin(admin.ModelAdmin):
#    list_display = ('classobj', "group_show", "group_access", "group_create",
#       "group_read", "group_update", "group_delete",
#       'id')
#    ordering=["classobj"]


@admin.register(DataSchema)
class DataSchemaAdmin(admin.ModelAdmin):
   list_display = ('classobj', 'keyname', 'displayname', 'dataformat', 'dataformat_ext', 'default_value', 
      'cardinal_min', 'cardinal_max', 'page', 'order', 'id')
   ordering=["classobj","order", "keyname"]
   list_filter = ["classobj"]


@admin.register(DataInstance)
class DataInstanceAdmin(admin.ModelAdmin):
   list_display = ('classobj', 'keyname', 'is_enabled', 'id')
   ordering=["classobj","keyname"]
   list_filter = ["classobj"]

