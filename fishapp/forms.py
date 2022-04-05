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


class TankDesignParametersForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TankDesignParametersForm,self).__init__(*args, **kwargs)
         # # in case no initial arumenr
        self.fields['usermodel'].widget.attrs['readonly']=True
        #self.fields['usermodel'].disabled=True    
    class Meta:
        model = TankDesignParameters
        fields = ['usermodel','tank_length', 'tank_width', 'depth', 'volume_of_water',   'density_per_cubic_metre', 
         'total_fish_per_tank_per_cycle','tank_num_of_months_per_cycle', 'fish_per_tank_per_year', 'num_of_tanks']

  

 