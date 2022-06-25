from django import forms

from django.forms import CheckboxSelectMultiple, ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.utils import get_current_user_groups
from .models import *

from django.db.models import Q


class BlogItemForm(forms.ModelForm): 
    
    class Meta:
        model = BlogItem
        fields = ['title','content']
    
  