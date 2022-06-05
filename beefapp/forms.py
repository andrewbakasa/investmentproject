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

    # def __init__(self, user=None, *args, **kwargs):
    #     super(FeedlotDesignParametersForm,self).__init__(*args, **kwargs)
       
    #     self.fields['pen_area'].widget.attrs['readonly']=True
    #     self.fields['sqm'].widget.attrs['readonly']=True
    #     self.fields['sqm_per_cattle'].widget.attrs['readonly']=True
    #     self.fields['cattle_per_pen_per_year'].widget.attrs['readonly']=True
    class Meta:
        model = FeedlotDesignParameters
        fields = ['usermodel','length', 'width',   'sqm_per_cattle', 
         'total_cattle_per_pen_per_cycle','num_of_months_per_cycle', 
        'num_of_feedlots', 
         'construction_cost_per_pen','machinery_cost_per_pen', 
         'building_cost_per_sqm','total_land_sqm','cost_of_land_per_sqm']


