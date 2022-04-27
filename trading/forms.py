from django import forms

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.utils import get_current_user_groups
from .models import *

from django.db.models import Q


class InvestorFormUpdate(forms.ModelForm):
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "3", #size
            'placeholder'   : 'description', 
            'style'         : 'resize : none' 
            }), required=False) 
     
    def __init__(self, *args, **kwargs):
        super(InvestorFormUpdate,self).__init__(*args, **kwargs)
       
       

    class Meta:
        model = Investor
        fields = ['investment','user','name', 'description','value' ]
    
class InvestorForm(forms.ModelForm): 
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "3", #size
            'placeholder'   : 'description', 
            'style'         : 'resize : none' 
            }), required=False)   
    
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvestorForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['user'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.user:
                self.fields['user']=initial_arguments.user
        
    
    class Meta:
        model = Investor
        fields = ['investment','user','name', 'description','value' ]
    
    def save(self, commit=True):
        transaction = super().save(commit)
        
        return transaction


class UserInvestmentForm(forms.ModelForm):
   
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "7", #size
            'placeholder'   : 'description', 
            'style'         : 'resize : none' 
            }), required=False)  

    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserInvestmentForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['creater'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.creater:
                self.fields['creater']=initial_arguments.creater
        
    
    class Meta:
        model = Investment
        fields = ['name','description','category', 'total_value','creater' ]
    
    def save(self, commit=True):
        transaction = super().save(commit)
        
        return transaction



class UserInvestmentFormUpdate(forms.ModelForm):
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "3", #size
            'placeholder'   : 'description', 
            'style'         : 'resize : none' 
            }), required=False) 
     
    def __init__(self, *args, **kwargs):
        super(UserInvestmentFormUpdate,self).__init__(*args, **kwargs)
       
       

    class Meta:
        model = Investment
        fields = ['name','description','category', 'total_value']
  