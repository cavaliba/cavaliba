# app_conf - models.py

from django.db import models

import datetime
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class SireneConfiguration(models.Model):

    appname = models.SlugField(_('Sirene App'), max_length=128, null=False, blank=False, default="home")
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
        verbose_name = "Sirene Configuration"
        verbose_name_plural = "Sirene Configurations"
        #unique_together = ('login', 'site',)


    def __str__(self):
        return self.keyname


