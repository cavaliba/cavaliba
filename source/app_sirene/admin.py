# (c) cavaliba.com - sirene - admin.py

from django.contrib import admin


from .models import MessageTemplate
from .models import Message
from .models import MessageUpdate
from .models import Category
from .models import PublicPage
from .models import PublicPageJournal

from .models import SMSJournal



# -----------------------------------
# Category
# ----------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    ordering=['id','name']
    list_display = ('name','longname', 'is_enabled', 'id')


# ------------------------------------------------------
# Public Pages
# ------------------------------------------------------

@admin.register(PublicPage)
class PublicPageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name','title','is_default','is_enabled')
    ordering=['id','name']
    #list_filter = ('category','severity','has_publicpage', 'has_privatepage', 'has_email','has_sms','is_enabled')
#    search_fields = ['name', 'amount','status']

# ------------------------------------------------------
# Public Pages Journal
# ------------------------------------------------------

@admin.register(PublicPageJournal)
class PublicPageJournalAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('created_at', 'created_by',  'removed_at', 'removed_by', 'is_visible', 'name','title','severity')
    ordering=['-created_at']
    #list_filter = ('category','severity','has_publicpage', 'has_privatepage', 'has_email','has_sms','is_enabled')
#    search_fields = ['name', 'amount','status']

# ------------------------------------------------------
# Message 
# ------------------------------------------------------

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name','title','category','severity', 'has_privatepage', 'has_email','has_sms','is_enabled')
    ordering=['id','name']
    list_filter = ('category','severity', 'has_privatepage', 'has_email','has_sms','is_enabled')
#    search_fields = ['name', 'amount','status']


# Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('created_at', 'updated_at','is_visible','created_by','title','severity',
        'has_publicpage', 'has_privatepage', 'has_email','has_sms')
    ordering=['-created_at']
    list_filter = ('is_visible','severity','has_publicpage', 'has_privatepage', 'has_email','has_sms')
#    search_fields = ['name', 'amount','status']


# Updates
@admin.register(MessageUpdate)
class MessageUpdateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('message','created_at','created_by', 'id')
    ordering=['-created_at']
    #list_filter = ('is_visible','severity','has_publicpage', 'has_privatepage', 'has_email','has_sms')
#    search_fields = ['name', 'amount','status']


# ------------------------------------------------------
# SMS Journal
# ------------------------------------------------------

@admin.register(SMSJournal)
class SMSJournalAdmin(admin.ModelAdmin):
    save_on_top = False
    list_display = ('created_at', 'created_by', 'mobile', 'quota',  'id')
#    list_filter = ('site', "name","is_enabled")
#    search_fields = ['name', 'amount','status']
    ordering=["-created_at"]
