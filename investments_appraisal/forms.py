from tabnanny import verbose
from django.forms import ModelForm
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.utils import get_current_user_groups
from .models import *
#from employees.models import CompanyUser
from django.forms.widgets import CheckboxSelectMultiple
from datetime import date, timedelta
from django.contrib.postgres.forms import SimpleArrayField

from django.db.models import Q
from django.contrib.auth.models import User
class InvestmentOptionsModelForm(forms.ModelForm):
    # cost_of_land_per_sqm = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000.0))
    # cost_of_machinery_per_pen = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # cost_of_building_per_sqm = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # cost_of_pen_construction = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # senior_debt_dynamic_parameter = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # initial_pens_employed = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # pen_cattle_density = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # pen_length = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # pen_width = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # pen_height = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
    # total_land_required = SimpleArrayField(forms.DecimalField(decimal_places=2, max_digits=10, default =1000))
   
    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(InvestmentOptionsModelForm,self).__init__(*args, **kwargs)
    #     user = user
    #      # # in case no initial arumenr
    #     self.fields['user'].widget.attrs['readonly']=True
    #     self.fields['user'].disabled=True
        
    
    class Meta:
        model = InvestmentOptions
        fields = ['usermodel','optionparameters']
   
    

class UserBusinessModelForm(forms.ModelForm):
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "6", #size
            'placeholder'   : 'write your model description', 
            'style'         : 'resize : none' 
            }), required=False)

    
    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserBusinessModelForm,self).__init__(*args, **kwargs)
        self.user_alias = user
       
        initial_arguments= kwargs.get('instance', None)
        self.fields['user'].widget.attrs['readonly']=True       
        # self.fields['user'].disabled=True
        if initial_arguments:
            if initial_arguments.user:
                # self.fields['user'].disabled=True
                self.fields['user']=initial_arguments.user
        
    
    class Meta:
        model = UserModel
        fields = ['model_type','name','description','user', 'currency']
    
    def save(self, commit=True):
        transaction = super().save(commit)
        
        return transaction

    def clean_name(self): 
        name = self.cleaned_data['name']
        user = self.user_alias
        if UserModel.objects.filter(Q(name = name) & Q(user = user) ).exists():
            record = UserModel.objects.filter(Q(name = name)& Q(user = user) ).first()
            dt= record.date_created.strftime('%d %b %Y') 
            model_type= record.model_type       
            raise ValidationError(_(f'You have a [{model_type}] model  with name [{name}] created on {dt}. Please rename this model to proceed'))
        return name



class UserModelFormUpdate(forms.ModelForm):
    description = forms.CharField(
            help_text=" Describe the description",#text to help
            widget=forms.Textarea( attrs={
            'cols'          : "30", #size
            'rows'          : "4", #size
            'placeholder'   : 'write your model description', 
            'style'         : 'resize : none' 
            }), required=False)
 
     
    def __init__(self, *args, **kwargs):
        super(UserModelFormUpdate,self).__init__(*args, **kwargs)
       
       
        #self.fields['user'].widget.attrs['readonly']=True   
        #print(self.fields['user'])    
        # self.fields['user'].disabled=True
        # if not self.check_if_premium_user():
        #     self.fields['simulation_run'].widget.attrs['readonly']=True

    class Meta:
        model = UserModel
        fields = ['name','description', 'model_type', 'currency', 
                 'simulation_iterations',  'user', 'simulation_run', 'npv_bin_size', 'total_params']
    
    def clean_simulation_iterations(self):
        simulation_iterations = self.cleaned_data['simulation_iterations']
        obj =SimulationParameters.objects.first()   
        if obj:
            val= obj.max_simulation_iter
        else:
            val=100

        if simulation_iterations>val:
          
            raise ValidationError(_(f'An model with {simulation_iterations} runs-is greather than allowed {val}'))
        return simulation_iterations

    def clean_simulation_run(self):
        simulation_run = self.cleaned_data['simulation_run']
        if simulation_run == True:
            if 'user' in self.cleaned_data:
                user = self.cleaned_data['user']
                user_group_set =get_current_user_groups(user)   
                premium_user = True if 'premium_user' in user_group_set else False
                if premium_user == False:
                    raise ValidationError(_(f'To have this right please upgrade your account'))
            else:
                raise ValidationError(_(f'User not specified'))
        return simulation_run

    def check_if_premium_user(self):
        if 'user' in self.cleaned_data:
            user = self.cleaned_data['user']
            user_group_set =get_current_user_groups(user)   
            premium_user = True if 'premium_user' in user_group_set else False
            return premium_user
        else:
            return False

    def clean_name(self): 
         #print(data)
        name = self.cleaned_data['name'] 
        if name != None:
            if 'user' in self.cleaned_data:
                user = self.cleaned_data['user']
                if UserModel.objects.filter(Q(name = name) & Q(user = user)).exists():
                    record = UserModel.objects.filter(Q(name = name)& Q(user = user)).first()
                    dt= record.date_created.strftime('%d %b %Y') 
                    model_type= record.model_type       
                    raise ValidationError(_(f'You have a [{model_type}] model  with name [{name}] created on {dt}. Please rename this model to proceed'))
                return name
        return name
  

class TimingAssumptionForm(forms.ModelForm):
 
    
    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(TimingAssumptionForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
    #     #self.fields['usermodel'].disabled=True   
    class Meta:
        model = TimingAssumption
        fields = ['usermodel','base_period','construction_start_year','construction_len',
        'construction_year_end',  'operation_start_year', 'operation_duration', 
        'operation_end','number_of_months_in_a_year']


   
class TimingAssumptionFormUpdate(forms.ModelForm):
   
    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(TimingAssumptionFormUpdate,self).__init__(*args, **kwargs)
    #     if user:
    #         pass
    
    class Meta:
        model = TimingAssumption
        fields = ['usermodel','base_period','construction_start_year','construction_len',
        'construction_year_end',  'operation_start_year', 'operation_duration', 
        'operation_end','number_of_months_in_a_year']
  
  
  


class PricesForm(forms.ModelForm):

    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(PricesForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
        #self.fields['usermodel'].disabled=True    
    class Meta:
        model = Prices
        fields = ['usermodel','title','base_price','change_in_price']

class DepreciationForm(forms.ModelForm):

    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(DepreciationForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
    #     #self.fields['usermodel'].disabled=True    
    class Meta:
        model = Depreciation
        fields = ['usermodel','economic_life_of_machinery',
        'economic_life_of_buildings','tax_life_of_machinery','tax_life_of_buildings',
        'tax_life_of_soft_capital_costs']
    


class TaxesForm(forms.ModelForm):

    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(TaxesForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
    #     #self.fields['usermodel'].disabled=True    
    class Meta:
        model = Taxes
        fields = ['usermodel','import_duty',
        'sales_tax','corporate_income_tax']
class FinancingForm(forms.ModelForm):

    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(FinancingForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
    #     #self.fields['usermodel'].disabled=True    
    class Meta:
        model = Financing
        fields = ['usermodel','real_interest_rate', 'risk_premium',
                  'num_of_installments','grace_period',  'equity','senior_debt']



class WorkingCapitalForm(forms.ModelForm):

    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(WorkingCapitalForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
    #     #self.fields['usermodel'].disabled=True    
    class Meta:
        model = WorkingCapital
        fields = ['usermodel','accounts_receivable', 'accounts_payable', 'cash_balance']


class MacroeconomicParametersForm(forms.ModelForm):

    # def __init__(self, user=None, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(MacroeconomicParametersForm,self).__init__(*args, **kwargs)
    #      # # in case no initial arumenr
    #     self.fields['usermodel'].widget.attrs['readonly']=True
    #     #self.fields['usermodel'].disabled=True    
    class Meta:
        model = MacroeconomicParameters
        fields = ['usermodel','discount_rate_equity', 'domestic_inflation_rate', 'us_inflation_rate',
                  'exchange_rate',    'dividend_payout_ratio', 'num_of_shares', 'investment_costs_over_run_factor']

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['perpage_blogs', 'perpage', 'pertable']
  
    def clean_pertable(self):
        pertable = self.cleaned_data['pertable']
        max_val=50
        min_val=3
        if pertable>max_val:
            raise ValidationError(_(f'{pertable} is greather than max allowed of {max_val}'))
        elif pertable <min_val:
            raise ValidationError(_(f'{pertable} is less than min allowed of {min_val}'))
        return pertable

    def clean_perpage(self):
        perpage = self.cleaned_data['perpage']
        max_val=50
        min_val=3
        if perpage>max_val:
            raise ValidationError(_(f'{perpage} is greather than max allowed of {max_val}'))
        elif perpage <min_val:
            raise ValidationError(_(f'{perpage} is less than min allowed of {min_val}'))
        return perpage

class UserProfileForm(forms.ModelForm):
    aboutyou = forms.CharField(
                help_text=" Describe the description",#text to help
                widget=forms.Textarea( attrs={
                'cols'          : "30", #size
                'rows'          : "4", #size
                'placeholder'   : 'About me', 
                'style'         : 'resize : none' 
                }), required=False)
    class Meta:
        model = UserProfile
        fields = ['age', 'country', 'sex', 'profession' ,'aboutyou', 'image']
class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']  
 
class PurchasePlanForm(forms.ModelForm):
    class Meta:
        model = PurchasePlan
        fields = ['name', 'email' ,'userplan']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email' ,'message' ,'subject']

class NewsSubscribeForm(forms.ModelForm):
    class Meta:
        model = NewsSubscribe
        fields = [ 'email' ]
    
  