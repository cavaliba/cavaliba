# # (c) cavaliba.com - sirene - forms.py

from django import forms
from django.utils.translation import gettext_lazy as _


from app_home.configuration import get_configuration

from .models import SIRENE_SEVERITY
from .models import Category
from .models import PublicPage

from app_user.models import SireneGroup

from app_data.models import DataClass
from app_data.models import DataInstance

from tinymce.widgets import TinyMCE



class MessageTemplateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        
        super(MessageTemplateForm, self).__init__(*args, **kwargs)

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


    is_enabled = forms.BooleanField(required=False,
        label=_("Enabled"),
        initial = True
        )

    name  = forms.SlugField(max_length=128, required=True,
        label = ("Unique Name"),
        widget=forms.TextInput(attrs={'size':40})
        )

    title  = forms.CharField(max_length=128, required=False,
        label = _("Title"),
        widget=forms.TextInput(attrs={'size':80})
        )

    category = forms.ModelChoiceField(
        label=_("Category"), 
        queryset=Category.objects.filter(is_enabled=True).order_by('id'),
        required=True,
        )

    severity = forms.ChoiceField(
        widget=forms.Select, choices=SIRENE_SEVERITY,
        label=_("Severity"), 
        )
    
    description = forms.CharField(max_length=250, required=False,
        label = _("Usage"),
        #widget=forms.TextInput(attrs={'size':80})
        widget=forms.Textarea(attrs={'rows':6, 'cols':80})
        )


    publicpage = forms.ModelChoiceField(
        label=_("Public Page"), 
        queryset=PublicPage.objects.filter(is_enabled=True, is_default=False).order_by('id'),
        required=False,
        )

    has_privatepage = forms.BooleanField(required=False, 
        label=_("Private page"),
        initial = False
        )

    has_email = forms.BooleanField(required=False, 
        label=_("Send emails"),
        initial = False
        )


    has_sms = forms.BooleanField(required=False, 
        label=_("Send SMS"),
        initial = False
        )



# -----


    notify_app = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify Apps"),
        help_text = _("Select Apps to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='app').first() ),
        queryset=DataInstance.objects.all(),
        widget=forms.SelectMultiple,
        )

    notify_site = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify Sites"),
        help_text = _("Select Sites to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='site').first() ),
        queryset=DataInstance.objects.all(),
        widget=forms.SelectMultiple,
        )

    notify_sitegroup = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify SiteGroups"),
        help_text = _("Select Sitegroups to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='sitegroup').first() ),
        queryset=DataInstance.objects.all(),
        widget=forms.SelectMultiple,
        )

    notify_customer = forms.ModelMultipleChoiceField(required=False,
        label=_("Notify Customers"),
        help_text = _("Select Customers to notify"),
        #queryset=DataInstance.objects.filter(classobj=DataClass.objects.filter(keyname='customer').first() ),
        queryset=DataInstance.objects.all(),
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

