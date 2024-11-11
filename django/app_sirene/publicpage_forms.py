# forms_publicpage.py

from django import forms

from .models import SIRENE_SEVERITY

from tinymce.widgets import TinyMCE

from .models import Category


class PublicPageForm(forms.Form):


	is_enabled = forms.BooleanField(required=False,
		label="Actif",
		initial = True
		)

	name  = forms.SlugField(max_length=128, required=True,
		label = "Nom unique (*)",
		widget=forms.TextInput(attrs={'size':40})
		)

	severity = forms.ChoiceField(
		label = "Sévérité",
		widget=forms.Select, 
		choices=SIRENE_SEVERITY
		)

	title  = forms.CharField(max_length=128, required=False,
		label = "Titre",
		widget=forms.TextInput(attrs={'size':80})
		)

	is_default = forms.BooleanField(required=False,
		label="Page par défaut",
		initial = False
		)

	body = forms.CharField(max_length=2500, required=False,
		label="Message",
		#widget=forms.Textarea(attrs={'cols':80})
		widget=TinyMCE(attrs={'cols': 60, 'rows': 30})
		)


