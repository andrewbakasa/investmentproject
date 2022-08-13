from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from . import  models

class ExportForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()
    accounts = forms.ModelMultipleChoiceField(
        queryset=models.Product.objects.all())