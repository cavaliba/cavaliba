# {{ app_name }} - models.py

from django.db import models

import datetime
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



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
# common
# ---------------------------------------


# APP_CHOICE = (
#      ("na", "n/a"),                # white
#      ("critical", "critical"),     # black
#      ("major", "major"),           # red
#      ("minor", "minor"),           # yellow
#      ("info", "info"),             # blue
#      ("other", "other"),           # grey
#      ("ok", "ok"),                 # green
# )



# ---------------------------------------
# Configuration
# ---------------------------------------

# class Configuration(models.Model):

#     key   = models.CharField('Key', max_length=100, blank=False, unique=True)
#     value = models.CharField('Value', max_length=1500, blank=True, default="")
#     page = models.CharField('Page', max_length=1500, blank=True, default="")
#     # format : int, string, json , password ?


#     def __str__(self):
#         return self.key


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

# class MyLog(models.Model):

#     created = models.DateTimeField(auto_now_add=True, db_index=True)   # , default=datetime.now
#     level = models.CharField('Level', choices=SIRENE_LOGLEVEL, max_length=20, default="na")
#     domain = models.CharField('Domain', max_length=200, default="na")
#     data = models.CharField('string', max_length=2000, default="")
#     username = models.CharField('Username', max_length=256, default="na")
#     user_ip = models.CharField('User IP', max_length=64, default="")

#     def __str__(self):
#         return self.data



# ---------------------------------------
# Category
# ---------------------------------------

# class Category(models.Model):
#     """Message category"""

#     name         = models.SlugField('Name (slug/unique)', max_length=50, blank=False, unique=True, default="na")
#     display     = models.CharField('Display name', max_length=128, blank=True)
#     description  = models.CharField('Description', max_length=500, blank=True)
#     is_enabled   = models.BooleanField('Enabled', default=True)


#     class Meta:
#         db_table = "{{ app_name}}_category"
#         ordering = ['id']
#         verbose_name = "Category"
#         verbose_name_plural = "Categories"

#     def __str__(self):
#         return f"{self.name}"





# ---------------------------------------
# # AAAProfil
# # ---------------------------------------

# class AAARole(models.Model):

#     name          = models.SlugField('Nom', max_length=128, unique=True)
#     description   = models.CharField('Description', max_length=500,  null=True, blank=True)
#     permissions   = models.ManyToManyField('AAAPermission', blank=True)
#     is_default    = models.BooleanField('Role par défaut', default=False)
#     is_enabled    = models.BooleanField('Actif', default=True)

#     class Meta:
#         ordering = ['name']
#         verbose_name = "AAA Role"
#         verbose_name_plural = "AAA Roles"

#     def __str__(self):
#         return f"{self.name}"


# # Static list of granular / atomic permission (list in code aaa_get)
# class AAAPermission(models.Model):

#     name  = models.CharField("Permission", max_length=128, unique=True)
#     description = models.CharField('Description', max_length=500,  null=True, blank=True)

#     class Meta:
#         #ordering = ['permission']
#         verbose_name = "AAA Permission"
#         verbose_name_plural = "AAA Permissions"

#     def __str__(self):
#         return "{} - {}".format(self.name ,self.description)


# ---------------------------------------
# API
# ---------------------------------------

# class APIKey(models.Model):

#     is_enabled    = models.BooleanField('Actif', default=True)
#     name          = models.SlugField('Nom', max_length=128, unique=True)
#     key           = models.CharField("Clé", max_length=64)
#     ips_allowed   = models.CharField("IPs autorisées", max_length=500, null=True, blank=True)
#     description   = models.CharField('Description', max_length=500,  null=True, blank=True)

#     class Meta:
#         ordering = ['name']
#         verbose_name = "API Key"
#         verbose_name_plural = "API Keys"

#     def __str__(self):
#         return "{} - {}".format(self.name ,self.description)