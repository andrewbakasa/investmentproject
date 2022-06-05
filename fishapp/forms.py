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

    # def __init__(self, user=None, *args, **kwargs):
    #     super(TankDesignParametersForm,self).__init__(*args, **kwargs)
       
    #     self.fields['volume_of_water'].widget.attrs['readonly']=True
    #     self.fields['density_per_cubic_metre'].widget.attrs['readonly']=True
    #     self.fields['fish_per_tank_per_year'].widget.attrs['readonly']=True
     
    class Meta:
        model = TankDesignParameters
        fields = ['usermodel','tank_length', 'tank_width', 'depth', 'volume_of_water',   
                  'density_per_cubic_metre', 'total_fish_per_tank_per_cycle',
                  'tank_num_of_months_per_cycle', 'fish_per_tank_per_year', 'num_of_tanks',                  
                  'purchase_price_tank','machinery_cost_per_tank', 
                  'building_cost_per_sqm','total_land_sqm','cost_of_land_per_sqm']

  

 