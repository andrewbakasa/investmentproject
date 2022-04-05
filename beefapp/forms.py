from django.forms import ModelForm
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import *
#from employees.models import CompanyUser
from django.forms.widgets import CheckboxSelectMultiple
from datetime import date, timedelta
from django.contrib.postgres.forms import SimpleArrayField

from django.db.models import Q

class FeedlotDesignParametersForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FeedlotDesignParametersForm,self).__init__(*args, **kwargs)
         # # in case no initial arumenr
        self.fields['usermodel'].widget.attrs['readonly']=True
        #self.fields['usermodel'].disabled=True    
    class Meta:
        model = FeedlotDesignParameters
        fields = ['usermodel','length', 'width', 'sqm', 'pen_area',   'sqm_per_cattle', 
         'total_cattle_per_pen_per_cycle','num_of_months_per_cycle', 'cattle_per_pen_per_year','num_of_feedlots']
