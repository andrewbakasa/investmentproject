from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
#from common.models import User
from .models import CompanyUser
from store.models import *
#from invoices.models import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms.widgets import CheckboxSelectMultiple
from store.models import ProductCategory
from django.db.models import Q
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductUpdateForm(forms.ModelForm):
    description = forms.CharField(
                    help_text=" Describe the product",#text to help
                    widget=forms.Textarea( attrs={
                    'cols'          : "30", #size
                    'rows'          : "3", #size
                    'placeholder'   : 'Description', 
                    'style'         : 'resize : none' 
                    }))
    class Meta:
        model = Product
        fields = ['shop', 'name', 'price', 'categories', 'description','image']
    
    def __init__(self, *args, **kwargs):
        #self.request = kwargs.pop('request', None)
        instance= kwargs.get('instance', None) 
        #print('Product>>>', instance)
        #print("kwargs",kwargs)
        user=None
        if instance:
            if instance.created_by:
                user=instance.created_by  
        #print(self.request,user)
        super(ProductUpdateForm,self).__init__(*args, **kwargs)
        #print('NNNNNN:', self.fields)
        #self.fields['shop'].widget.attrs['readonly']=True
        if user:
             self.fields['shop'].queryset = Shop.objects.filter(Q(user = user))
        # else:
        #     self.fields['shop'].queryset= None

class ProductForm(forms.ModelForm):
    description = forms.CharField(
                    help_text=" Describe the product",#text to help
                    widget=forms.Textarea( attrs={
                    'cols'          : "30", #size
                    'rows'          : "3", #size
                    'placeholder'   : 'Description', 
                    'style'         : 'resize : none' 
                    }))
    class Meta:
        model = Product
        fields = ['shop', 'name', 'price', 'categories', 'description','image','created_by']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        initial_arguments= kwargs.get('initial', None) 
        #print("kwargs",kwargs)
        user=None
        if initial_arguments:
            if initial_arguments['created_by']:
                user=initial_arguments['created_by']

        super(ProductForm,self).__init__(*args, **kwargs)
        
        #print('NNNNNN:', self.fields)
        if user:
            self.fields['shop'].queryset = Shop.objects.filter(Q(user = user))
        # else:
        #     self.fields['shop'].queryset= None
  
    # def clean_image(self):
    #     image = self.cleaned_data.get('image', None) 
    #     if image:
    #         # do some validation, if it fails
    #         raise forms.ValidationError(u'Form error')
    #     return image


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'address1','address2', 'email', 'phone', 'coporateclient']

class ExportForm(forms.Form):
    EXPORT_SELECT = (       
        ('web', 'web'),
            ('csv', 'csv'), 
    )

    export_type = forms.ChoiceField(label='Select Type', choices=EXPORT_SELECT)

    
    company = forms.ModelMultipleChoiceField(
            queryset=Company.objects.all(), widget=forms.CheckboxSelectMultiple(
            attrs= {'class':'column-checkbox'}
            ),)
            # ,"style":"height:100px;overflow:scroll;"

    def __init__(self, user=None, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ExportForm,self).__init__(*args, **kwargs)
        if user:
            user_company= CompanyUser.objects.filter(user=user)
            item_sbu =[]
            if user_company :
                #manytomany link by pk
                item_sbu = list(user_company.values_list('company', flat=True))

           
            self.fields['company'].queryset = Company.objects.filter(pk__in=item_sbu) 
            # self.fields['company'].widget.attrs.update({'class':'scrollbar-y'}) 
            

       
        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Field(Div('company', css_class="scrollbar-y")),
        # )

