from django.db import models

#import datetime
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



from app_user.models import SireneUser
from app_user.models import SireneGroup

from app_data.models import DataClass
from app_data.models import DataInstance

# ---------------------------------------
# common
# ---------------------------------------


SIRENE_SEVERITY = (
     ("na", _("n/a")),                # white
     ("critical", _("critical")),     # black
     ("major", _("major")),           # red
     ("minor", _("minor")),           # yellow
     ("info", _("info")),             # blue
     ("other", _("other")),           # grey
     ("ok", _("ok")),                 # green
)



# ---------------------------------------
# Category
# ---------------------------------------

class Category(models.Model):
    """Message category"""

    name         = models.SlugField(_("Name"), max_length=128, blank=False, unique=True, default="na")
    longname     = models.CharField(_("Display name"), max_length=128, blank=True)
    description  = models.CharField(_("Description"), max_length=500, blank=True)
    is_enabled   = models.BooleanField(_("Enabled"), default=True)


    class Meta:
        ordering = ['id']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


# ---------------------------------------
# PublicPages
# ---------------------------------------

class PublicPage(models.Model):

    name         = models.SlugField(_("Name"), max_length=128, blank=False, unique=True)
    title        = models.CharField(_('Title'), max_length=250, blank=True)
    body         = models.TextField(_('Text'), max_length=2500, blank=True)
    severity     = models.CharField(_('Severity'), choices=SIRENE_SEVERITY, max_length=20, default="na")
    is_default   = models.BooleanField(_('Default Public Page'), default=False)
    is_enabled   = models.BooleanField(_('Enabled'), default=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Public Page"
        verbose_name_plural = "Public Pages"

    def __str__(self):
        return self.name


class PublicPageJournal(models.Model):

    name             = models.SlugField(_('Name'), max_length=128, blank=False)
    title            = models.CharField(_('Title'), max_length=250, blank=True)
    body             = models.TextField(('Text'), max_length=2500, blank=True)
    severity         = models.CharField(_('Severity'), choices=SIRENE_SEVERITY, max_length=20, default="na")
    is_default       = models.BooleanField(_('Default Public Page'), default=False)
    is_visible = models.BooleanField(_('Is visible'), default=True, db_index=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=False, db_index=True)   # , default=datetime.now
    created_by = models.CharField(_('Created by'), max_length=200, blank=True)
    removed_at = models.DateTimeField(_("Removed at"), auto_now_add=False, blank=True, null=True)
    removed_by = models.CharField(_('Removed by'), max_length=200, blank=True, default='auto')


    class Meta:
        ordering = ['name']
        verbose_name = "Public Page Journal"
        verbose_name_plural = "Public Pages Journal"

    def __str__(self):
        return "{} ({} - {})".format(self.name, self.severity, self.title )


    def remove(self, aaa=None):

        self.is_visible = False
        self.removed_at = timezone.now()
        if aaa:
            self.removed_by = aaa.get("username", "auto")
        else:
            self.removed_by = "auto"
        self.save()


    @classmethod
    def reset(cls, aaa=None):
        ''' remove all active public pages entries in the journal'''

        entries = cls.objects.filter(is_visible=True)
        for entry in entries:
            entry.remove(aaa)


    @classmethod
    def add(cls, publicpage=None, aaa=None):

        if not publicpage:
            return

        journal = cls()
        journal.name = publicpage.name
        journal.title = publicpage.title
        journal.body = publicpage.body
        journal.severity = publicpage.severity
        journal.is_default = publicpage.is_default
        journal.created_at = timezone.now()
        journal.created_by = aaa.get("username", "n/a")

        try:
            journal.save()
            return journal
        except Exception as e:
            return None



# ---------------------------------------
# Templates
# ---------------------------------------

class MessageTemplate(models.Model):

    name             = models.SlugField(_('Name'), max_length=128, blank=False, unique=True)
    category         = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    severity         = models.CharField(_('Severity'), choices=SIRENE_SEVERITY, max_length=20)
    is_enabled       = models.BooleanField(_('Enabled'), default=True)

    title            = models.CharField(_('Title'), max_length=250, blank=True)
    body             = models.TextField(_('Message'), max_length=5000, blank=True)
    description      = models.TextField(_('Description'), max_length=2500, blank=True)

    publicpage       = models.ForeignKey(PublicPage, null=True, blank=True, on_delete=models.SET_NULL)

    has_publicpage   = models.BooleanField(_('Public Page'), default=False)
    has_privatepage  = models.BooleanField(_('Private Page'), default=False)
    has_email        = models.BooleanField(_('Email'), default=False)
    has_sms          = models.BooleanField(_('SMS'), default=False)

    
    notify_site      = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_app       = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_sitegroup = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_customer  = models.ManyToManyField(DataInstance, related_name="+", blank=True)

    # additional groups
    notify_group     = models.ManyToManyField(SireneGroup, related_name="+", blank=True)
    


    class Meta:
        ordering = ['name']
        verbose_name = "MessageTemplate"
        verbose_name_plural = "MessageTemplates"

    def __str__(self):
        return "{} - {}".format(self.name, self.title )


# ---------------------------------------
# Messages 
# ---------------------------------------


class Message(models.Model):

    category         = models.CharField(_('Category'), max_length=128, default="?", blank=True) 
    severity         = models.CharField(_('Severity'), choices=SIRENE_SEVERITY, max_length=20, default="na")

    title            = models.CharField(_('Title'), max_length=250, blank=True)
    body             = models.TextField(_('Message'), max_length=5000, blank=True)

    publicpage_text  = models.TextField(_('Public page text'), max_length=2500, blank=True)
    publicpage       = models.ForeignKey(PublicPageJournal, null=True, blank=True, on_delete=models.SET_NULL)

    has_publicpage   = models.BooleanField(_('Private Page'), default=False)
    has_privatepage  = models.BooleanField(_('Private Page'), default=False)
    has_email        = models.BooleanField(_('Email'), default=False)
    has_sms          = models.BooleanField(_('SMS'), default=False)

    email_count = models.IntegerField(_('Emails sent'), default=0)
    sms_count = models.IntegerField(_('SMS sent'), default=0)

    is_visible = models.BooleanField(_('Visible'), default=True, db_index=True)
    
    template         = models.CharField(_('Template'), max_length=80, blank=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, db_index=True)   # , default=datetime.now
    updated_at = models.DateTimeField(_('Updated at'), null=True, blank=True, db_index=True)
    removed_at = models.DateTimeField(_("Removed at"), auto_now_add=False, blank=True, null=True)

    created_by = models.CharField(_('Created by'), max_length=200, blank=True)
    updated_by = models.CharField(_('Updated by'), max_length=200, blank=True)
    removed_by = models.CharField(_('Removed by'), max_length=200, blank=True)

    # for MessageUpdate new notifications
    notify_customer  = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_site      = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_app       = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_sitegroup = models.ManyToManyField(DataInstance, related_name="+", blank=True)
    notify_group     = models.ManyToManyField(SireneGroup, related_name="+", blank=True)
    
    # auto populated
    notify_text      = models.TextField(_('Message (text)'), blank=True)
    # individual users notified
    users            = models.ManyToManyField(SireneUser, related_name="+", blank=True)
    users_text       = models.TextField(_('Users (text)'), blank=True)

    class Meta:
        ordering = ['created_at','severity']
        verbose_name = "Message"
        verbose_name_plural = "Messages"


    def __str__(self):
        return "{} - {} - {}".format(self.title, self.category, self.severity )


    def remove(self, aaa=None):

        self.is_visible = False
        self.removed_at = timezone.now()
        if aaa:
            self.removed_by = aaa.get("username", "auto")
        else:
            self.removed_by = "auto"
        self.save()

        # also remove associated PublicPageJournal entry
        if self.publicpage:
            self.publicpage.remove(aaa=aaa)


class MessageUpdate(models.Model):

    message    = models.ForeignKey(Message, related_name="updates", on_delete=models.CASCADE)
    content    = models.TextField(_('Message'), max_length=5000, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)   # , default=datetime.now
    created_by = models.CharField(_('created by'), max_length=200, blank=True)
    has_email  = models.BooleanField(_('Email'), default=False)
    has_sms    = models.BooleanField(_('SMS'), default=False)

    class Meta:
        ordering = ['created_at','created_by']
        verbose_name = "Message Update"
        verbose_name_plural = "Message Updates"

    def __str__(self):
        return f"{self.created_at}"

# ---------------------------------------
# SMS Journal
# ---------------------------------------

class SMSJournal(models.Model):

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, db_index=True)   # , default=datetime.now
    created_by = models.CharField(_('Created by'), max_length=200, blank=True)
    mobile     = models.CharField(_('Mobile'), max_length=32, null=True, blank=True)
    content    = models.TextField(_('Content'), max_length=5000, blank=True)
    quota      = models.IntegerField(_('Quota left'), null=True, blank=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "SMS Journal"
        verbose_name_plural = "SMS Journal"

    def __str__(self):
        return f"{self.created_at} - {self.mobile}"
