# (c) cavaliba.com - IAM - models.py

from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# ---------------------------------------
# SireneUser
# ---------------------------------------

class SireneUser(models.Model):

    login  = models.CharField(_('Login/Identifier(*)'), max_length=128, unique=True, blank=False)
    external_id = models.CharField(_('External ID'), max_length=128, null=True, blank=True) 

    email = models.CharField(_('Email'), max_length=128, null=True, blank=True)
    mobile = models.CharField(_('Mobile'), max_length=32, null=True, blank=True)
    firstname = models.CharField(_('Firstname'), max_length=128, null=True, blank=True)
    lastname = models.CharField(_('Lastname'), max_length=128, null=True, blank=True)
    displayname = models.CharField(_("Display name"), max_length=500,  null=True, blank=True)

    description = models.CharField(_('Description'), max_length=500, null=True, blank=True)
    is_enabled = models.BooleanField(_('Enabled'), default=True)
    last_login = models.DateTimeField(_("Last Login"), auto_now_add=False, blank=True, null=True)

    # Sirene Prefs 
    want_notifications = models.BooleanField(_('Want Notifications'), default=True)
    want_24 = models.BooleanField(_('Want 24/24'), default=True)
    want_sms = models.BooleanField(_('Want SMS'), default=False)
    want_email = models.BooleanField(_('Want Email'), default=True)
    secondary_email  = models.CharField(_('Secondary Email'), max_length=128, null=True, blank=True)
    secondary_mobile  = models.CharField(_('Secondary Mobile'), max_length=128, null=True, blank=True)

    last_update = models.DateTimeField(_("Last update"), auto_now_add=False, blank=True, null=True)


    class Meta:
        ordering = ['login']
        verbose_name = "Sirene User"
        verbose_name_plural = "Sirene Users"
        #unique_together = ('login', 'site',)
        indexes = [
            models.Index(fields=["login"]),
            models.Index(fields=["is_enabled"]),
            models.Index(fields=["displayname"]),
            models.Index(fields=["email"]),
            ]


    def __str__(self):
        if self.displayname:
            return "{} - {}".format(self.login ,self.displayname )
        else:
            return "{}".format(self.login)


# ---------------------------------------
# SireneGroup & Role
# ---------------------------------------

class SireneGroup(models.Model):
    keyname      = models.SlugField(_('Keyname(*)'), max_length=128, blank=False, unique=True,)
    displayname  = models.CharField(_("Display name"), max_length=500,  null=True, blank=True)
    description  = models.CharField(_('Description'), max_length=500,  null=True, blank=True)
    is_enabled   = models.BooleanField(_('Enabled'), default=True)
    is_role      = models.BooleanField(_('Role'), default=False)
    is_builtin   = models.BooleanField(_('Built-in group'), default=False)
    users        = models.ManyToManyField(SireneUser, blank=True)
    subgroups    = models.ManyToManyField('self', symmetrical=False, blank=True)
    #roles        = models.ManyToManyField('SireneRole', blank=True)
    permissions  = models.ManyToManyField('SirenePermission', blank=True)

    last_update = models.DateTimeField(_("Last update"), auto_now_add=False, blank=True, null=True)


    class Meta:
        ordering = ['keyname']
        verbose_name = "Sirene Group"
        verbose_name_plural = "Sirene Groups"
        indexes = [
            models.Index(fields=["keyname"]),
            models.Index(fields=["is_enabled"]),
            models.Index(fields=["is_role"]),
            ]

    def __str__(self):
        return "{}".format(self.keyname )


# RBAC
# -------------------------
# SireneUser => SireneGroup (0..N)  =>  || => SireneRole (0..N) <= SirenePermission
# Roles are provided by each app (or global if app is Null)
# Roles are set of granular Permissions
# granular / atomic permission provided by each app
# p_xxx_permision[_c|_r|_u|_d|...]
# ex. p_home_access

class SirenePermission(models.Model):

    keyname     = models.SlugField(_('Permission(*)'), max_length=128, blank=False, unique=True )
    appname     = models.SlugField(_('Sirene App'), max_length=128, null=True, blank=True )
    displayname = models.CharField(_("Display name"), max_length=500,  null=True, blank=True)
    description = models.CharField('Description', max_length=500,  null=True, blank=True)
    is_builtin  = models.BooleanField(_('Built-in permission'), default=False)
    default     = models.BooleanField(_('Allowed by default'), default=False)


    class Meta:
        ordering = ['keyname']
        verbose_name = "Sirene Permission"
        verbose_name_plural = "Sirene Permissions"
        indexes = [
            models.Index(fields=["keyname"]),
            models.Index(fields=["appname"]),
            ]


    def __str__(self):
        return f"{self.keyname}"


# -----------------------------------------------------------------------------
# Sirene Visitor
# ------------------------------------------------------------------------------
class SireneVisitor(models.Model):

    username   = models.CharField(_('Username'), max_length=255, unique=True, blank=False)
    user_ip    = models.CharField(_('Visitor IP'), max_length=64, default="")
    last_login = models.DateTimeField("Last Login", auto_now_add=False, blank=True, null=True)


    class Meta:
        ordering = ['last_login']
        verbose_name = "Sirene Visitor"
        verbose_name_plural = "Sirene Visitors"
        indexes = [
            models.Index(fields=["username"]),
            ]


    def __str__(self):
        return self.username




