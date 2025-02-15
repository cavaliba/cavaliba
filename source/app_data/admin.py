# (c) cavaliba.com - data - admin.py

from django.contrib import admin

from app_data.models import DataClass
from app_data.models import DataSchema
from app_data.models import DataInstance


@admin.register(DataClass)
class DataClassAdmin(admin.ModelAdmin):
   list_display = ('keyname', 'displayname', 'is_bigset', 'count_estimation', 'order', 'page', 'is_enabled', 'p_read', 'id')
   ordering=["keyname"]
   list_filter = ["page"]

@admin.register(DataSchema)
class DataSchemaAdmin(admin.ModelAdmin):
   list_display = ('classobj', 'keyname', 'displayname', 'dataformat', 'dataformat_ext', 'default_value', 
      'cardinal_min', 'cardinal_max', 'page', 'order', 'id')
   ordering=["classobj","order", "keyname"]
   list_filter = ["classobj"]


@admin.register(DataInstance)
class DataInstanceAdmin(admin.ModelAdmin):
   list_display = ('classobj', 'keyname', 'is_enabled', 'p_read', 'id')
   ordering=["classobj","keyname"]
   list_filter = ["classobj"]

