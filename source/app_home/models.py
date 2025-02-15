# (c) cavaliba.com - home - models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

from app_user.models import SirenePermission


# ---------------------------------------
# Dashboard
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
    #page  = models.CharField('Page', max_length=128, blank=True, default="")
    sidebar_section  = models.CharField('Sidebar section', max_length=128, blank=True, default="")
    dashboard_section  = models.CharField('Dashboard section', max_length=128, blank=True, default="")
    order = models.IntegerField('Order', default=100)
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


# ---------------------------------------
# Logs
# ---------------------------------------

class CavalibaLog(models.Model):

    app = models.CharField(_('App'), max_length=200, blank=True, default="")
    view = models.CharField(_('View'), max_length=200, blank=True, default="")
    action = models.CharField(_('Action'), max_length=200, blank=True, default="")
    status = models.CharField(_('Status'), max_length=32, blank=True, default="")
    data = models.CharField(_('data'), max_length=2000, default="")
    
    level = models.CharField(_('Level'), max_length=20, default="na")
    created = models.DateTimeField(auto_now_add=True, db_index=True)   # , default=datetime.now
    
    #domain = models.CharField('Domain', max_length=200, default="na")
    
    username = models.CharField(_('Username'), max_length=256, default="na")
    user_ip = models.CharField(_('User IP'), max_length=64, default="")
    impersonate = models.CharField(_('Impersonate'), max_length=256, default="na")

    class Meta:
        #db_table = "{{ app_name}}_category"
        ordering = ['created']
        verbose_name = "Cavaliba Log"
        verbose_name_plural = "Cavaliba Logs"

    def __str__(self):
        return f"{self.created}/{self.username}({self.impersonate})/{self.user_ip} - {self.level}/{self.status} - {self.app}/{self.view}/{self.action}"


class CavalibaAPIStat(models.Model):

    keyname       = models.SlugField(_('Keyname'), max_length=128, unique=True)
    last_success = models.DateTimeField(_("Last success"), auto_now_add=False, blank=True, null=True)
    last_error   = models.DateTimeField(_("Last error"), auto_now_add=False, blank=True, null=True)
    success_count  = models.IntegerField(_("success count"), default=0)
    error_count  = models.IntegerField(_("Error count"), default=0)

    class Meta:
        verbose_name = "Cavaliba API Stat"
        verbose_name_plural = "Cavaliba API Stats"
        indexes = [
            models.Index(fields=["keyname"]),
            ]

    def __str__(self):
        return f"{self.keyname}"
