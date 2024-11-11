# app_home - models.py

from django.db import models

import datetime
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from app_user.models import SirenePermission
# EXAMPLE
# name             = models.SlugField('Name (slug,unique)', max_length=50, blank=False, unique=True)
# title            = models.CharField('Title', max_length=250, blank=True)
# body             = models.TextField('Text', max_length=2500, blank=True)
# severity         = models.CharField('Severity', choices=SIRENE_SEVERITY, max_length=20, default="na")
# is_default       = models.BooleanField('Default Public Page', default=False)
# is_enabled       = models.BooleanField('Enabled', default=True)
# is_visible = models.BooleanField('Is visible', default=True, db_index=True)
# created_at = models.DateTimeField("Created at", auto_now_add=False, db_index=True)   # , default=datetime.now
# created_by = models.CharField('Created by', max_length=200, blank=True)
# removed_at = models.DateTimeField("Removed at", auto_now_add=False, blank=True, null=True)
# removed_by = models.CharField('Removed by', max_length=200, blank=True, default='auto')
# severity         = models.CharField('Sévérité', choices=SIRENE_SEVERITY, max_length=20, default="na")
# site             = models.ForeignKey("Site", null=True, blank=True, on_delete=models.SET_NULL)
# notify_to        = models.ManyToManyField(Scope, blank=True)
# IntegerField
# FloatField
# JSONField
# => https://docs.djangoproject.com/en/5.0/ref/models/fields/


# ---------------------------------------
# DashApp
# ---------------------------------------

DASHBOARD_APP_STATE = (
     ("enabled", "enabled"),
     ("disabled", "disabled"),
     ("hidden", "hidden"),
)

class DashboardApp(models.Model):

    keyname   = models.SlugField('Key name(*)', max_length=100, blank=False, unique=True)
    displayname  = models.CharField('Display name', max_length=128, blank=True)
    description  = models.CharField('Description', max_length=500, blank=True)
    is_enabled  = models.BooleanField(_('Enabled'), default=True)
    url   = models.CharField('URL', max_length=1500, blank=True, default="")
    icon  = models.CharField('Icon', max_length=128, blank=True, default="")
    page  = models.CharField('Page', max_length=128, blank=True, default="")
    order = models.IntegerField('Order', default=100)
    #state = models.CharField('State', choices=DASHBOARD_APP_STATE, max_length=20, default="enabled")
    #version  = models.CharField('Version', max_length=128, blank=True, default="")
    permission = models.ForeignKey(SirenePermission, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "app_home_dashboard_app"
        ordering = ['order']
        verbose_name = "Dashboard Application"
        verbose_name_plural = "Dashboard Applications"

    def __str__(self):
        return self.keyname


# ---------------------------------------
# Configuration
# ---------------------------------------

class CavalibaConfiguration(models.Model):

    appname = models.SlugField(_('Cavaliba App'), max_length=128, null=False, blank=False, default="home")
    keyname = models.SlugField(_('Keyname(*)'), max_length=128, null=False, blank=False)

    value   = models.CharField(_('Value'), max_length=1500, blank=True, null=True)

    description  = models.CharField(_('Description'), max_length=500,  null=True, blank=True)
    page    = models.CharField(_('Page'), max_length=1500, blank=True, default="")
    order   = models.IntegerField(_('Order'), default=100)

    # group
    # type : int/string/json/IP/...
    # default value ?

    class Meta:
        unique_together = ["appname", "keyname"]
        ordering = ['appname', 'page', 'order', 'keyname']
        verbose_name = "Cavaliba Configuration"
        verbose_name_plural = "Cavaliba Configurations"
        #unique_together = ('login', 'site',)


    def __str__(self):
        return self.keyname

