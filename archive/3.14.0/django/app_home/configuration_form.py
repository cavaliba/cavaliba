# configuration_forms.py

from django import forms
from django.utils.translation import gettext as _



# -----------------------------------------------------------------
# commin
# -----------------------------------------------------------------

CHOICE_YES_NO = (
    ("no", "no"), 
    ("yes", "yes")
)


# -----------------------------------------------------------------
# HOME
# -----------------------------------------------------------------


class AppHomeConfigurationForm(forms.Form):


    GLOBAL_APPNAME  = forms.CharField(max_length=128, 
        required=False,
        label = "GLOBAL_APPNAME",
        help_text = _("Global application name for display"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    CSV_DELIMITER  = forms.CharField(
        max_length=1, 
        required=False,
        label = "CSV_DELIMITER",
        help_text = _("Default value is ;"),
        widget=forms.TextInput(attrs={'size':1}),
        )

    # logo size in navbar if not 0 ; home icon otherwise
    LOGO_SIZE = forms.IntegerField( 
        required=False,
        label = "LOGO_SIZE",
        help_text = _("Logo size in navbar ; use 0 to display icon."),
        )

    LOG_KEEP_DAYS = forms.IntegerField( 
        required=False,
        label = "LOG_KEEP_DAYS",
        help_text = _("Number of days of logs to keep in database (default: 31)"),
        )

    LOG_DEBUG = forms.ChoiceField(
        choices = (("yes", "yes"), ("no","no")),
        label = "LOG_DEBUG",
        help_text = _("Do you want to enable logging for debug level ?"),
        )


    BETA_PREVIEW = forms.ChoiceField(
        choices = CHOICE_YES_NO,
        required=False,
        label = "BETA_PREVIEW",
        help_text = _("Beta/Preview features (unstable)"),
        )



# -----------------------------------------------------------------
# USER
# -----------------------------------------------------------------

class AppUserConfigurationForm(forms.Form):


    CHOICE_AUTH_MODE = (
        ("basic", "basic"), 
        ("oauth2", "oauth2"),
        ("forced", "forced"),
        ("local", "local"),
    )
    AUTH_MODE = forms.ChoiceField(
        choices = CHOICE_AUTH_MODE,
        required=False,
        label = "AUTH_MODE",
        help_text = _("Authentication mechanism."),
        )

    AUTH_MODE_FORCE_USER  = forms.CharField(max_length=128, 
        label = "AUTH_MODE_FORCE_USER",
        help_text = _("Login to use if AUTH_MODE is forced"),
        widget=forms.TextInput(attrs={'size':60}),
        )


    AUTH_FEDERATED_LOGIN_FIELD  = forms.CharField(max_length=128, 
        label = "AUTH_FEDERATED_LOGIN_FIELD",
        help_text = _("Token field name for login (default: X-User)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    AUTH_FEDERATED_EMAIL_FIELD  = forms.CharField(max_length=128, 
        label = "AUTH_FEDERATED_EMAIL_FIELD",
        help_text = _("Token field name for email (default: X-Email)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    AUTH_LOGIN_REMOVE_DOMAIN = forms.CharField(max_length=128, 
        label = "AUTH_LOGIN_REMOVE_DOMAIN",
        help_text = _("Remove domain name from login ; yes/no (default: yes)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    CHOICE_AUTH_PROVISIONING = (
        ("manual", "manual"), 
        ("visitor", "visitor"),
        ("create", "create"),
        ("update", "update"),
        ("sync", "sync")
    )
    AUTH_PROVISIONING = forms.ChoiceField(
        choices = CHOICE_AUTH_PROVISIONING,
        required=False,
        label = "AUTH_JUST_IN_TIME",
        help_text = _("Allow / Create user dynamically if authenticated exteranlly but not in DB "),
        )
    TRUSTED_ANONYMOUS_IPS = forms.CharField(max_length=128,
        required = False,
        label = "TRUSTED_ANONYMOUS_IPS",
        help_text = _("Allowed IP/CIDR for anonymous access, comma separated"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    DEBUG_AAA = forms.ChoiceField(
        choices = CHOICE_YES_NO,
        required=False,
        label = "DEBUG_AAA",
        help_text = _("Display AAA debug information"),
        )
    DEBUG_AAA2 = forms.ChoiceField(
        choices = CHOICE_YES_NO,
        required=False,
        label = "DEBUG_AAA2",
        help_text = _("Display additional AAA debug information, groups, perms, ...."),
        )
    CACHE_SESSION = forms.ChoiceField(
        choices = CHOICE_YES_NO,
        required=False,
        label = "Cache Sessions",
        help_text = _("Use session cache (performance)"),
        )


    SYSADMIN_IMPERSONATE = forms.CharField(max_length=128,
        required = False,
        label = "SYSADMIN_IMPERSONATE",
        help_text = _("Login to impersonate if admin"),
        widget=forms.TextInput(attrs={'size':60}),
        )


# -----------------------------------------------------------------
# DATA
# -----------------------------------------------------------------

class AppDataConfigurationForm(forms.Form):

    DATA_DEFAULT_SIZE = forms.IntegerField( 
        required=False,
        label = "DATA_DEFAULT_SIZE",
        help_text = _("Default number of entries per page"),
        )

    DATA_MAX_SIZE = forms.IntegerField( 
        required=False,
        label = "DATA_MAX_SIZE",
        help_text = _("Max number of entries per page"),
        )

    DATA_BIGSET_SIZE = forms.IntegerField( 
        required=False,
        label = "DATA_BIGSET_SIZE",
        help_text = _("Max size before using partial lists and ajax queries"),
        )

    EXPORT_INTERACTIVE_MAX_SIZE = forms.IntegerField( 
        required=False,
        label = "EXPORT_INTERACTIVE_MAX_SIZE",
        help_text = _("Max dataset size for interactive export"),
        )




# -----------------------------------------------------------------
# SIRENE
# -----------------------------------------------------------------

class AppSireneConfigurationForm(forms.Form):


    SIRENE_APPNAME  = forms.CharField(max_length=128, 
        required=False,
        label = "SIRENE_APPNAME",
        help_text = _("Display name on public pages"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    PUBLIC_MAX_ITEMS = forms.IntegerField( 
        required=False,
        label = "PUBLIC_MAX_ITEMS",
        help_text = _("Max number of public messages to display (default: 5)"),
        )


    PUBLIC_MAX_MINUTES = forms.IntegerField( 
        required=False,
        label = "PUBLIC_MAX_MINUTES",
        help_text = _("Duration in minutes for public message display (default: 1440, 24h)"),
        )


    PUBLIC_SORT_ORDER_CHOICES = (
        ("creation", "creation"), 
        ("severity", "severity")
    )
    PUBLIC_SORT_ORDER = forms.ChoiceField(choices = PUBLIC_SORT_ORDER_CHOICES,
        required=False,
        label = "PUBLIC_SORT_ORDER",
        help_text = _("Display order of public messages"),
        )

    # PUBLIC_SKIP_TO_TRUSTED = forms.BooleanField( 
    #     label = "PUBLIC_SKIP_TO_TRUSTED",
    #     help_text = "If trusted IP, don't display Public Page, skip to Anonymous/trusted page directly",
    #     )

    PUBLIC_SKIP_TO_TRUSTED = forms.ChoiceField(
        choices = (("yes", "yes"), ("no","no")),
        label = "PUBLIC_SKIP_TO_TRUSTED",
        help_text = _("If trusted IP, don't display Public Page, skip to Anonymous/trusted page directly"),
        )


    PRIVATE_MAX_MINUTES = forms.IntegerField( 
        required=False,
        label = "PRIVATE_MAX_MINUTES",
        help_text = _("Duration in minutes for private message display (default: 1440, 24h)"),
        )


    CHOICE_EMAIL_MODE = (
        ("stdout", "stdout"), 
        ("folder", "folder"), 
        ("smtp", "smtp"),
    )
    EMAIL_MODE = forms.ChoiceField(
        choices = CHOICE_EMAIL_MODE,
        required=False,
        label = "EMAIL_MODE",
        help_text = _("How to send email"),
        )

    EMAIL_FOLDER = forms.CharField(
        max_length=128, 
        required=False,
        label = "EMAIL_FOLDER",
        help_text = _("Email Folder (email mode folder)"),
        widget=forms.TextInput(attrs={'size':60}),
        )


    EMAIL_FROM = forms.CharField(
        max_length=128, 
        required=False,
        label = "EMAIL_FROM",
        help_text = _("Source email address"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    EMAIL_SMTP_BATCH = forms.IntegerField( 
        required=False,
        label = "EMAIL_SMTP_BATCH",
        help_text = _("Max number of dest per SMTP connection"),
        )
    
    EMAIL_PREFIX  = forms.CharField(max_length=128, 
        label = "EMAIL_PREFIX",
        help_text = _("Email prefix for new messages (default: [Sirene] )"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    EMAIL_UPDATE_PREFIX  = forms.CharField(max_length=128, 
        label = "EMAIL_UPDATE_PREFIX",
        help_text = _("Email prefix for update messages (default: [Sirene Update] )"),
        widget=forms.TextInput(attrs={'size':60}),
        )


    EMAIL_TEST_SUBJECT  = forms.CharField(max_length=128, 
        label = "EMAIL_TEST_SUBJECT",
        help_text = _("Email subject for test messages"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    EMAIL_TEST_CONTENT  = forms.CharField(max_length=256, 
        label = "EMAIL_TEST_CONTENT",
        help_text = _("Email content for test messages"),
        widget=forms.Textarea(attrs={'cols':60})
        )


    SMS_QUOTA_PER_DAY = forms.IntegerField( 
        required=False,
        label = "SMS_QUOTA_PER_DAY",
        help_text = _("Quota of SMS per user, per 24h (default: 100)"),
        )

    CHOICE_SMS_MODE = (
        ("stdout", "stdout"), 
        ("folder", "folder"),
        ("clicsecure", "clicsecure"),
    )
    SMS_MODE = forms.ChoiceField(
        choices = CHOICE_SMS_MODE,
        required=False,
        label = "SMS_MODE",
        help_text = _("SMS API"),
        )

    SMS_FOLDER = forms.CharField(
        max_length=128, 
        required=False,
        label = "SMS_FOLDER",
        help_text = _("SMS Folder (sms mode folder)"),
        widget=forms.TextInput(attrs={'size':60}),
        )


    SMS_PREFIX  = forms.CharField(max_length=128, 
        label = "SMS_PREFIX",
        help_text = _("SMS prefix (default: [Sirene] )"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    SMS_UPDATE_PREFIX  = forms.CharField(max_length=128, 
        label = "SMS_UPDATE_PREFIX",
        help_text = _("SMS prefix for updates (default: [Sirene Update] )"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    SMS_TEST  = forms.CharField(max_length=128, 
        label = "SMS_TEST",
        help_text = _("SMS test content"),
        widget=forms.TextInput(attrs={'size':60}),
        )

# class

    APP_CLASS  = forms.CharField(max_length=128, 
        label = "APP_CLASS",
        help_text = _("Data Class name for apps (app)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    SITE_CLASS  = forms.CharField(max_length=128, 
        label = "SITE_CLASS",
        help_text = _("Data Class name for sites (site)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    SITEGROUP_CLASS  = forms.CharField(max_length=128, 
        label = "SITEGROUP_CLASS",
        help_text = _("Data Class name for sitegroups (sitegroup)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    CUSTOMER_CLASS  = forms.CharField(max_length=128, 
        label = "CUSTOMER_CLASS",
        help_text = _("Data Class name for customers (customer)"),
        widget=forms.TextInput(attrs={'size':60}),
        )

