# (c) cavaliba.com - IAM - forms.py

from django import forms
from django.utils.translation import gettext as _

from .models import SireneUser
from .models import SireneGroup
from .models import SirenePermission


class UserForm(forms.Form):

    is_enabled = forms.BooleanField(required=False,
        label="Actif",
        initial = True
        )


    login  = forms.CharField(max_length=128, required=True,
        label = _("Login/ID(*)"),
        help_text = _("Unique, login or contact name"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    firstname   = forms.CharField(max_length=128, required=False,
        label = _("Firstname"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    lastname   = forms.CharField(max_length=128, required=False,
        label = _("Lastname"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    displayname   = forms.CharField(max_length=128, required=False,
        label = _("Display name"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    groups = forms.ModelMultipleChoiceField(required=False,
        label = _("Groups"),
        help_text = _("Select groups for this user."),
        queryset=SireneGroup.objects.exclude(is_role=True).filter(is_enabled=True),
        widget=forms.SelectMultiple
        )

    email  = forms.EmailField(max_length=128, required=False,
        label = _("Email"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    mobile = forms.CharField(max_length=128, required=False,
        label = _("Mobile"),
        help_text = _("Mobile number for SMS"),        
        widget=forms.TextInput(attrs={'size':60}),
        )

    description = forms.CharField(max_length=250, required=False,
        label = _("Description"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    want_notifications = forms.BooleanField(required=False,
        label = _("Notifications"),
        help_text = _("Select to receive notifications"),
        initial = True
        )
        
    want_24 = forms.BooleanField(required=False,
        label = _("Notifications 24/7"),
        help_text = _("Select to receive notifications outside of business hours"),
        initial = True
        )

    want_email = forms.BooleanField(required=False,
        label = _("Notifications by Email"),
        help_text = _("Select to receive notifications by email"),
        initial = True
        )
        
    want_sms = forms.BooleanField(required=False,
        label = _("Notifications by SMS"),
        help_text = _("Select to receive notifications by SMS"),
        initial = False
        )

    secondary_email  = forms.EmailField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label = _("Secondary Email"),
        help_text = _("Will be used instead of main email address"),
        )
    
    secondary_mobile = forms.CharField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label = _("Secondary Mobile SMS number"),
        help_text = _("Will be used instead of main SMS number"),
        )



# File Import Form
class UserUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        ),
        label="Fichier",
        help_text = "Choose a file with users (yaml,json)",
        )




# User Preferences
class UserPrefForm(forms.Form):


    email  = forms.EmailField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        disabled=True,
        label=_("Primary email address"),
        help_text = _("This email receives notifications if no secondary email is provided"),
        )

    mobile = forms.CharField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        disabled=True,
        label=_("Mobile phone number"),
        help_text = _("This mobile receives SMS notifications if no secondary number is provided"),
        )

    firstname   = forms.CharField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label=_("Firstname"),
        )
    lastname   = forms.CharField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label=_("Lastname"),
        )
    displayname   = forms.CharField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label=_("Display name"),
        help_text = _("Use a Firstname Lastname format or similar"),
        )

    want_notifications = forms.BooleanField(required=False,
        label=_("Enable Notifications"),
        help_text = _("Select to be included in notifications"),
        )
        
    want_24 = forms.BooleanField(required=False,
        label=_("Enable 24/7 notifications"),
        help_text = _("Select to receive notifications outside of business hours"),
        )

    want_email = forms.BooleanField(required=False,
        label=_("Enable email notifications"),
        help_text = _("Select to receive notifications by email"),
        )
        
    want_sms = forms.BooleanField(required=False,
        label=_("Enable SMS notifications"),
        help_text = _("Select to receive notifications by SMS"),
        )

    secondary_email  = forms.EmailField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label=_("Secondary Email address"),
        help_text = _("If provdided, will be used instead of primary address"),
        )
    
    secondary_mobile = forms.CharField(max_length=128, required=False,
        widget=forms.TextInput(attrs={'size':60}),
        label=_("Secondary mobile phone number"),
        help_text = _("If provdided, will be used instead of primary mobile"),
        )   


# ----------------------------------------------------------
# Groups
# ----------------------------------------------------------
class GroupForm(forms.Form):

    is_enabled = forms.BooleanField(required=False,
        label = _("Enabled"),
        initial = True
        )

    is_builtin = forms.BooleanField(required=False,
        label = _("Built-in"),
        initial = False,
        disabled = True,
        )


    keyname  = forms.SlugField(max_length=128, required=True,
        label = _("Keyname(*)"),
        help_text = _("unique, no special chars"),
        widget=forms.TextInput(attrs={'size':80})
        )

    displayname   = forms.CharField(max_length=128, required=False,
        label = _("Display name"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    description = forms.CharField(max_length=250, required=False,
        label = _("Description"),
        widget=forms.TextInput(attrs={'size':80})
        )

    subgroups = forms.ModelMultipleChoiceField(required=False,
        label = _("Subgroups"),
        help_text = _("Select sub-groups members of this group."),
        queryset=SireneGroup.objects.exclude(is_role=True).filter(is_enabled=True),
        widget=forms.SelectMultiple
        )



# File Import Form
class GroupUploadForm(forms.Form):

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        ),
        label="File",
        help_text = "Choose a file with groups (yaml,json)",
        )


# ----------------------------------------------------------
# Role
# ----------------------------------------------------------
class RoleForm(forms.Form):


    is_enabled = forms.BooleanField(required=False,
        label = _("Enabled"),
        initial = True
        )

    is_builtin = forms.BooleanField(required=False,
        label = _("Built-in"),
        initial = False,
        disabled = True,
        )

    is_role = forms.BooleanField(required=False,
        label = _("Security/Role"),
        initial = True
        )

    keyname  = forms.SlugField(max_length=128, required=True,
        label = _("Keyname(*)"),
        help_text = _("unique, no special chars"),
        widget=forms.TextInput(attrs={'size':80})
        )

    displayname   = forms.CharField(max_length=128, required=False,
        label = _("Display name"),
        widget=forms.TextInput(attrs={'size':60}),
        )

    description = forms.CharField(max_length=250, required=False,
        label = _("Description"),
        widget=forms.TextInput(attrs={'size':80})
        )

    subgroups = forms.ModelMultipleChoiceField(required=False,
        label = _("Subgroups"),
        help_text = _("Select groups with this role."),
        queryset=SireneGroup.objects.filter(is_enabled=True),
        widget=forms.SelectMultiple
        )


    permissions = forms.ModelMultipleChoiceField(required=False,
        label = _("Permissions"),
        help_text = _("Permissions for this role"),
        queryset=SirenePermission.objects.all(),
        widget=forms.SelectMultiple
        )



# File Import Form
class RoleUploadForm(forms.Form):

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        ),
        label="File",
        help_text = "Choose a file with roles (yaml,json)",
        )

