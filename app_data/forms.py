# app_data forms.py

from django import forms
from django.utils.translation import gettext as _


class DataUploadForm(forms.Form):

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        ),
        label="Fichier",
        help_text = "Choose a file with Sirene DATA (csv,yaml,json)",
        )


