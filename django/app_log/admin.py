# app_log - admin.py

from django.contrib import admin


from app_log.models import SireneLog


@admin.register(SireneLog)
class SireneLogAdmin(admin.ModelAdmin):
    list_display = ('created','username', 'user_ip', 'level','app','view','action','status', 'data')
    ordering=['created']
    list_filter = ["app","status"]
    #search_fields = ['name', 'amount','status']
