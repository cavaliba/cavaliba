
from django import forms
from django.utils.translation import gettext_lazy as _



class SMSForm(forms.Form):

    mobile = forms.CharField(
        max_length=12, 
        required=True,
        widget=forms.TextInput(attrs={'size':20}),
        label = _("Mobile number"),
        help_text = _("Provide a phone numer")
        )


    message  = forms.CharField(
        max_length=128, 
        required=True,
        label = _("Message"),
        widget=forms.Textarea(attrs={"rows":5, "cols":80}),
        )

