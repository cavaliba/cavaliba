# app_log - models.py

from django.db import models
from django.utils.translation import gettext_lazy as _


import datetime
from datetime import datetime
from datetime import timedelta
from django.utils import timezone



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
    # notify_to        = models.ManyToManyField(Scope, blank=True)
    # severity         = models.CharField('Sévérité', choices=SIRENE_SEVERITY, max_length=20, default="na")
    # site          = models.ForeignKey("Site", null=True, blank=True, on_delete=models.SET_NULL)



# ---------------------------------------
# MyLog
# ---------------------------------------

# SIRENE_LOGLEVEL = (
#      ("na",      "n/a"),
#      ("alert",   "1-alert"),
#      ("error",   "2-error"),
#      ("warning", "3-warning"),
#      ("info",    "4-info"),
#      ("debug",   "5-debug"),
# )

class SireneLog(models.Model):

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


    class Meta:
        #db_table = "{{ app_name}}_category"
        ordering = ['created']
        verbose_name = "Sirene Log"
        verbose_name_plural = "Sirene Logs"

    def __str__(self):
        return f"{self.created}/{self.username}/{self.user_ip} - {self.level}/{self.status} - {self.app}/{self.view}/{self.action}"

