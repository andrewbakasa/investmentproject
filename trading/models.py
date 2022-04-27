from __future__ import unicode_literals
import datetime
from os import access
from unicodedata import category

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
#from common.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date
# from store.models import Currency
from django.contrib.postgres.fields import ArrayField
import pandas as pd

from django.contrib.sessions.models import Session
from common.get_current_user import get_username
from investments_appraisal.middlewares import get_request

class InvestmentCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    uniqueid = models.CharField(max_length=200, unique=True)# beef01, fish01, 
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)# downloads
    	
    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
    
   
class Investment(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('InvestmentCategory', on_delete=models.SET_NULL, null=True,verbose_name="Category")
    likes = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)# downloads
    total_value = models.IntegerField(default=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name 

    @property
    def details(self):
        
        item = self.investmentdetails
        dict_ ={}
        dict_['strategy']=item.strategy if item.strategy else ""
        dict_['summary']=item.summary if item.summary else ""
        dict_['roi']=item.roi if item.roi else ""
        dict_['shareholding']=item.shareholding if item.shareholding else ""

        
        return dict_
    @property
    def investors_count(self):
        return self.investor_set.count()
    
    @property
    def current_investment(self):
        total = 0
        investments = self.investor_set.all()

        for investment in investments:
            total += investment.value 

        return total
    
    
    def userIsInvestor(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            return True

        return False
    
    def userIsInvestorAttr(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            return 'myinvestment'

        return ''
   
class InvestmentDetails(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    strategy = models.TextField(blank=True,null=True)
    summary = models.TextField(blank=True,null=True)
    roi = models.TextField(blank=True,null=True)
    shareholding = models.TextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   	
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.investment) 
  
class Investor(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.SET_NULL, null=True) 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, verbose_name='Title')
    description = models.TextField(verbose_name='Investment Proposal')
    value= models.IntegerField(default= 0, verbose_name='Funds Pledge')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name 
    
    @property
    def trading_df(self):
        investments_df = pd.DataFrame(Investment.objects.all().values())	
        investors_df = pd.DataFrame(Investor.objects.filter(user=self.user).values())
        users_df = pd.DataFrame(User.objects.all().values())
        categories_df = pd.DataFrame(InvestmentCategory.objects.all().values()) 

        df = pd.DataFrame(columns =['fail_date','loco'])
        if investments_df.shape[0]>0 and investors_df.shape[0] > 0 : 
            investments_df['investment_id'] = investments_df['id']
            # mwrge
            df =pd.merge(investments_df, investors_df, on='investment_id',how="left").drop(['id_x',
                        'likes','hits','date_created_y','date_created_x','description_y'
                        ,'name_y','user_id','investment_id'], axis=1).rename(
                        {'id_y': 'retain_id','description_x':'summary', 'value':'myinvest', 
                        'name_x':'inv_name' }, axis=1)

            if users_df.shape[0]>0:
                users_df['creater_id'] = users_df['id']
                # merge
                df =pd.merge(df, users_df, on='creater_id',how="left").drop([
                    'id',  'password', 'last_login', 'is_superuser',
                    'is_staff', 'is_active',  'date_joined'
                ], axis=1).rename(
                            {}, axis=1)

            if categories_df.shape[0]>0:
                categories_df['category_id'] = categories_df['id']
                # merge
                df =pd.merge(df, categories_df, on='category_id',how="left").drop([
                    'date_created', 'likes', 'hits', 'creater_id', 'category_id','id'
                ], axis=1).rename(
                            {'description':'cat_descript','name':'cat_name', 'retain_id':'id'}, axis=1)

                            

            # 'inv_name', 'summary',  'total_value',
            # 'username', 'first_name', 'last_name', 'email', 'id', 'cat_name',
            # 'cat_descript', 'uniqueid'
        else:
            return df
        return df

class Enterprenuer(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name 



