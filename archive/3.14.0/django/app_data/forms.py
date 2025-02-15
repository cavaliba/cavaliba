# app_data forms.py

from django import forms
from django.utils.translation import gettext as _


class DataUploadForm(forms.Form):

    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs=None),
        #widget=forms.FileInput(attrs={'class': 'form-control-file'}),        
        label= _("File"),
        help_text = _("Choose a file (csv,yaml,json)"),
        )


