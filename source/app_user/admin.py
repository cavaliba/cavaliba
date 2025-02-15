# (c) cavaliba.cm - IAM - admin.py

from django.contrib import admin

from app_user.models import SireneUser
from app_user.models import SireneGroup
from app_user.models import SirenePermission
from app_user.models import SireneVisitor

# ----------------------------------

@admin.register(SireneUser)
class SireneUserAdmin(admin.ModelAdmin):
    list_display = ('login','displayname','email','external_id', 'is_enabled', 'id')
    ordering=['login']
    list_filter = ["is_enabled"]
    search_fields = ['login', 'displayname']

@admin.register(SireneGroup)
class SireneGroupAdmin(admin.ModelAdmin):
    list_display = ('keyname','displayname','is_role', 'is_builtin', 'is_enabled', 'id')
    ordering=['keyname']
    list_filter = ["is_enabled", "is_role","is_builtin"]
    search_fields = ['keyname', 'displayname']


@admin.register(SirenePermission)
class SirenePermissionAdmin(admin.ModelAdmin):
    list_display = ('appname','keyname', 'default', 'displayname', 'is_builtin','id')
    ordering=['appname', 'keyname']
    list_filter = ["appname", "default"]


@admin.register(SireneVisitor)
class SireneVisitorAdmin(admin.ModelAdmin):
    list_display = ('username','last_login','user_ip', 'id')
    ordering=['last_login']
#    list_filter = ["is_enabled"]



