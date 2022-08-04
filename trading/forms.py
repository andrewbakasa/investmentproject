from django import forms

from django.forms import CheckboxSelectMultiple, ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.utils import get_current_user_groups
from .models import *

from django.db.models import Q


class InvestorFormUpdate(forms.ModelForm):
    motivation = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "5", #size
            'placeholder'   : 'motivation', 
            'style'         : 'resize : none' 
            }), required=False) 
     
    def __init__(self, *args, **kwargs):
        super(InvestorFormUpdate,self).__init__(*args, **kwargs)
       
       

    class Meta:
        model = Investor
        fields = ['investment','user','name', 'motivation','value' ]
    
class InvestorForm(forms.ModelForm): 
    motivation = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "3", #size
            'placeholder'   : 'motivation', 
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
        fields = ['investment','user','name', 'motivation','value' ]
    
    def save(self, commit=True):
        transaction = super().save(commit)
        
        return transaction



from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField

class CustomSelectMultiple(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" %(obj.name)

class UserInvestmentForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(
            # attrs= {'class':'column-checkbox'}
            ),)
    
  
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "4", #size
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
        fields = ['name','description','category', 'total_value','creater', 'tags', 'public', 'closing_date' ]
       
    def clean_total_value(self):
        total_value = self.cleaned_data['total_value']
        max_val=50
        min_val=1
       
        if total_value < min_val:
            raise ValidationError(_(f'{total_value} is less than min allowed of {min_val}'))
        return total_value
    def save(self, commit=True):
        transaction = super().save(commit)
        
        return transaction



class UserInvestmentFormUpdate(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(
                # attrs= {'class':'column-checkbox'} 
            ),)
    
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
        fields = ['name','description','category', 'total_value', 'tags', 'public', 'closing_date']
  

    def clean_total_value(self):
        total_value = self.cleaned_data['total_value']
        max_val=50
        min_val=1
       
        if total_value < min_val:
            raise ValidationError(_(f'{total_value} is less than min allowed of {min_val}'))
        return total_value 

class InvestmentDetailsForm(forms.ModelForm):   
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvestmentDetailsForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['investment'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.investment:
                self.fields['investment']=initial_arguments.investment     
    class Meta:
        model = InvestmentDetails
        fields = ['investment','strategy','summary', 'roi','shareholding']
    
class InvestmentDetailsFormUpdate(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(InvestmentDetailsFormUpdate,self).__init__(*args, **kwargs)
    class Meta:
        model = InvestmentDetails
        fields = ['investment','strategy','summary', 'roi','shareholding']
  


class InvestmentSummaryForm(forms.ModelForm):   
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvestmentSummaryForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['investment'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.investment:
                self.fields['investment']=initial_arguments.investment     
    class Meta:
        model = InvestmentDetails
        fields = ['investment','summary']
    
class InvestmentSummaryFormUpdate(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(InvestmentSummaryFormUpdate,self).__init__(*args, **kwargs)
    class Meta:
        model = InvestmentDetails
        fields = ['investment','summary',]

class InvestmentStrategyForm(forms.ModelForm):   
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvestmentStrategyForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['investment'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.investment:
                self.fields['investment']=initial_arguments.investment     
    class Meta:
        model = InvestmentDetails
        fields = ['investment','strategy']
    
class InvestmentStrategyFormUpdate(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(InvestmentStrategyFormUpdate,self).__init__(*args, **kwargs)
    class Meta:
        model = InvestmentDetails
        fields = ['investment','strategy',]


class InvestmentShareholdingForm(forms.ModelForm):   
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvestmentShareholdingForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['investment'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.investment:
                self.fields['investment']=initial_arguments.investment     
    class Meta:
        model = InvestmentDetails
        fields = ['investment','shareholding']
    
class InvestmentShareholdingFormUpdate(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(InvestmentShareholdingFormUpdate,self).__init__(*args, **kwargs)
    class Meta:
        model = InvestmentDetails
        fields = ['investment','shareholding',]

class InvestmentROIForm(forms.ModelForm):   
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(InvestmentROIForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['investment'].widget.attrs['readonly']=True  
        if initial_arguments:
            if initial_arguments.investment:
                self.fields['investment']=initial_arguments.investment     
    class Meta:
        model = InvestmentDetails
        fields = ['investment','roi']
    
class InvestmentROIFormUpdate(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(InvestmentROIFormUpdate,self).__init__(*args, **kwargs)
    class Meta:
        model = InvestmentDetails
        fields = ['investment','roi',]

class InvestorStatusUpdate(forms.ModelForm):
    AC = [('verification', 'verification'),('accepted', 'accepted'), ('rejected', 'rejected')]
    
    # if engaged.... can only reject....
    def get_allowed_choices(self, state):
        allowed_status =[]
        if state=='pending':
            allowed_status= [('verification', 'verification'),('accepted', 'accepted'), ('rejected', 'rejected')]
         
        elif state=='verification':
            allowed_status= [('accepted', 'accepted'), ('rejected', 'rejected')]
       
        elif state=='accepted' or state=='engagement':
            allowed_status= [('rejected', 'rejected')]
        
        elif state=='rejected':
            allowed_status= [('accepted', 'accepted')]
      
        return allowed_status

    def check_value_in_list(self, list_ , test_val):
        for item in list_:
            if item[0]==test_val:
                return True
        return False
    def __init__(self, user=None, *args, **kwargs):
        super(InvestorStatusUpdate,self).__init__(*args, **kwargs)
        if not user==None:
            #LIMIT OPTIONS IF NOT SUPERUSER
            #ENGAGEMENT is handshake between two people: investor and enterprenuer
            #PENDING is for anything not seen yet...
            if not user.is_superuser:
                if self.instance:
                    allowed_choices= self.get_allowed_choices(self.instance.application_status)#[choice for choice in self.AC]
                    if self.check_value_in_list(allowed_choices,self.instance.application_status)==False:
                        allowed_choices.append((self.instance.application_status,self.instance.application_status))
                   
                    self.fields['application_status'].choices = allowed_choices
                else:
                    self.fields['application_status'].choices = self.AC
            else:
                #super user
                pass
               
        else:
            #Default
            if self.instance:
                # allowed_choices= [
                #         choice for choice in self.AC
                #         #if choice[0] != self.instance.application_status #exclude selected
                #     ]
                allowed_choices= self.get_allowed_choices(self.instance.application_status)
                #include current chpoice if not already there
                if self.check_value_in_list(allowed_choices,self.instance.application_status)==False:
                    allowed_choices.append((self.instance.application_status,self.instance.application_status))

                self.fields['application_status'].choices = allowed_choices
            else:
                self.fields['application_status'].choices = self.AC

    class Meta:
        model = Investor
        fields = ['application_status']

class InvestorStatusUpdateAjax(forms.ModelForm):
     
  
          
    class Meta:
        model = Investor
        fields = ['application_status']





     


