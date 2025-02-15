# forms_category.py

from django import forms
from django.utils.translation import gettext as _


class CategoryForm(forms.Form):

    
    is_enabled = forms.BooleanField(required=False,
        label=_("Enabled"),
        initial = True
        )

    name  = forms.SlugField(max_length=128, required=True,
        label = "Label (*)"
        )

    longname  = forms.CharField(max_length=128, required=False,
        label = _("Title"),
        widget=forms.TextInput(attrs={'size':80})

        )

    description = forms.CharField(max_length=250, required=False,
        label = _("Description"),
        widget=forms.TextInput(attrs={'size':80})
        )
