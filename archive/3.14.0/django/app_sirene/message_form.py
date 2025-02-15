# message_forms.py

from django import forms
from django.utils.translation import gettext as _

from tinymce.widgets import TinyMCE


from app_home.configuration import get_configuration


from .models import SIRENE_SEVERITY
from .models import Category
from .models import PublicPage
#from .models import MessageUpdate

from app_user.models import SireneGroup

from app_data.models import DataClass
from app_data.models import DataInstance


class MessageForm(forms.Form):

    # bar = forms.ModelChoiceField(queryset=Bar.objects.none())

    def __init__(self, *args, **kwargs):
        

        super(MessageForm, self).__init__(*args, **kwargs)

        classname = get_configuration("sirene","APP_CLASS")
        classobj = DataClass.objects.filter(keyname=classname).first()
        qs_app = DataInstance.objects.filter(classobj=classobj)

        classname = get_configuration("sirene","SITE_CLASS")
        classobj = DataClass.objects.filter(keyname=classname).first()
        qs_site = DataInstance.objects.filter(classobj=classobj)

        classname = get_configuration("sirene","SITEGROUP_CLASS")
        classobj = DataClass.objects.filter(keyname=classname).first()
        qs_sitegroup = DataInstance.objects.filter(classobj=classobj)

        classname = get_configuration("sirene","CUSTOMER_CLASS")
        classobj = DataClass.objects.filter(keyname=classname).first()
        qs_customer = DataInstance.objects.filter(classobj=classobj)
        

        self.fields['notify_app'].queryset = qs_app
        self.fields['notify_site'].queryset = qs_site
        self.fields['notify_sitegroup'].queryset = qs_sitegroup
        self.fields['notify_customer'].queryset = qs_customer


    title  = forms.CharField(max_length=128, required=False,
        label = "Titre",
        widget=forms.TextInput(attrs={'size':80})
        )

    category = forms.ModelChoiceField(
        required=True,
        label="Catégorie", 
        queryset=Category.objects.filter(is_enabled=True).order_by('id'),
        )

    severity = forms.ChoiceField(
        widget=forms.Select, choices=SIRENE_SEVERITY,
        label="Severité", 
        )
    

    publicpage = forms.ModelChoiceField(
        label="Page publique", 
        queryset=PublicPage.objects.filter(is_enabled=True, is_default=False).order_by('id'),
        required=False,
        )

    has_privatepage = forms.BooleanField(required=False, 
        label="Page privée globale",
        initial = False
        )

    has_email = forms.BooleanField(required=False, 
        label="Envoi d'Email",
        initial = False
        )

    has_sms = forms.BooleanField(required=False, 
        label="Envoi de SMS",
        initial = False
        )


    notify_app = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify Apps"),
        help_text = _("Select Apps to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='app').first() ),
        #queryset=DataInstance.objects.all(),
        queryset=DataInstance.objects.none(),
        widget=forms.SelectMultiple,
        )

    notify_site = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify Sites"),
        help_text = _("Select Sites to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='site').first() ),
        #queryset=DataInstance.objects.all(),
        queryset=DataInstance.objects.none(),
        widget=forms.SelectMultiple,
        )

    notify_sitegroup = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify SiteGroups"),
        help_text = _("Select Sitegroups to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='sitegroup').first() ),
        #queryset=DataInstance.objects.all(),
        queryset=DataInstance.objects.none(),
        widget=forms.SelectMultiple,
        )

    notify_customer = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify Customers"),
        help_text = _("Select Customers to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='customer').first() ),
        #queryset=DataInstance.objects.all(),
        queryset=DataInstance.objects.none(),
        widget=forms.SelectMultiple,
        )

    notify_group = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify User Groups"),
        help_text = _("Select additional User Groups to notify"),
        queryset=SireneGroup.objects.filter(is_enabled=True),
        widget=forms.SelectMultiple,
        )

# ----

    body = forms.CharField(max_length=2500, required=False,
        label="Message",
        #widget=forms.Textarea(attrs={'cols':80})
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
        )

# hidden, but has to be sent to template for header/display
    description = forms.CharField(max_length=2500, required=False,
        label="Description",
        disabled = True,
        widget=forms.HiddenInput()
        )

# ----------------

class MessageUpdateForm(forms.Form):

    has_email = forms.BooleanField(required=False,
        label="Notification Email",
        initial = False
        )

    has_sms = forms.BooleanField(required=False,
        label="Notification SMS",
        initial = False
        )


    content = forms.CharField(max_length=5000, required=False,
        label="Mise à jour",
        #widget=forms.Textarea(attrs={'cols':80})
        widget=TinyMCE(attrs={'cols': 60, 'rows': 30})
        )
