from __future__ import unicode_literals
import datetime
import math
from os import access

from unicodedata import category

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
#from common.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta 
from django.utils import timezone
# from store.models import Currency
from django.contrib.postgres.fields import ArrayField
import pandas as pd

from django.contrib.sessions.models import Session
from common.get_current_user import get_username
from investments_appraisal.middlewares import get_request
from django.db.models import Q
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
    
class Tag(models.Model):
    name = models.CharField(max_length=200,unique=True, null=True)

    def __str__(self):
        return self.name

   
class Investment(models.Model):
    name = models.CharField(max_length=60, verbose_name='title')
    description = models.TextField(null=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('InvestmentCategory', on_delete=models.SET_NULL, null=True,verbose_name="Category")
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0, verbose_name='Views')# downloads
    total_value = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, null=True, blank =True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)    
    closing_date = models.DateField(default=datetime.date.today() + timedelta(days=60), null=True)
    
    public= models.BooleanField(default=True)
    class Meta:
        ordering = ['-views']

    def __str__(self):
        return self.name 
    
    
    @property
    def time_to_close_attr(self):
        if self.closing_date > datetime.date.today():
            return 'Closing in: ' + str((self.closing_date - datetime.date.today()).days) + ' days'
        else:
            return  'Closed: ' +str((datetime.date.today()-self.closing_date).days) + ' days ago'
    
    @property
    def time_to_close(self):
        if self.closing_date > datetime.date.today():
            #
            return str((self.closing_date - datetime.date.today()).days) + ' days'
        else:
            return  str((datetime.date.today()-self.closing_date).days) + ' days'
    
    @property
    def closed_status(self):
        if self.closing_date > datetime.date.today():
            return False 
        else:
            return  True
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
    def incoming_investors(self):       
        return self.investor_set.filter(Q(application_status ="pending")).count()
        

    @property
    def current_investment(self):
        total = 0
        investments = self.investor_set.all()

        for investment in investments:
            total += investment.value 

        return total
    
    @property
    def accepted_investment(self):
        total = 0
        acc_investments = self.investor_set.filter(Q(application_status ="accepted"))

        for investment in acc_investments:
            total += investment.value 

        return total
    @property
    def current_investment_percent(self):
        percent = 0
        curr = self.current_investment
        if self.total_value !=0:
            percent= curr*100/self.total_value 
        
       
            if percent < 1:
                percent= round(percent,2)
            else:
                #==remove commas for any percent greater than 1
                percent= int(percent)
        # between 0-100
        return str(min(max(percent,0),100))
   
    @property
    def accepted_investment_percent(self):
        percent = 0
        curr = self.accepted_investment
        if self.total_value !=0:
            percent= curr*100/self.total_value 
        
       
            if percent < 1:
                percent= round(percent,2)
            else:
                #==remove commas for any percent greater than 1
                percent= int(percent)
        # between 0-100
        return str(min(max(percent,0),100))
    def userIsInvestor(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            return True

        return False
    
    def userIsInvestor_2(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            return True, qs

        return False, _

    def userIsOwnerAttr(self, user):  
        if self.creater == user :
            return 'myportifolio'

        return 'portifolio_na'

    def userIsOwner(self, user):    
        if self.creater == user :
            return True

        return False
    def userIsInvestorStatement(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            return 'I am an Investor [' + qs.application_status  +']'

        return 'I am NOT an Investor'

    def userIsInvestorAttr(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            #print(qs.application_status)
            # + recieved or pending, etc
            return 'myinvestment ' + str(qs.application_status)

        return 'myinvestment_na'
    
    def userIsInvestorRejectedAttr(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            #print(qs.application_status)
            # + recieved or pending, etc
            if qs.application_status =='rejected':
                return 'rejected ' #+ str(qs.application_status)

        return 'rejected_na'
    def userInvestorValue(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            return qs.value

        return 0

    def userInvestorPercent(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            percent = 0
            user_val = qs.value
            if self.total_value !=0:
                percent = user_val*100/self.total_value
                if percent < 1:
                    percent= round(percent,2)
                else:
                    #==remove commas for any percent greater than 1
                    percent= int(percent)
            # between 0-100
            return str(min(max(percent,0),100)) + '%'

        return 0


    def userIsInvestorStake(self, user):       
        qs = self.investor_set.filter(user=user).first()
        if qs:
            curr = self.current_investment
            max_val = max(self.total_value,curr)
            if max_val !=0:
                return round(qs.value*100/max_val,1)
            else:
                return 0

        return 0

    @property
    def blogs_count(self): 
        if  hasattr(self,'investmentblog'):   
            item = self.investmentblog
            return item.blogitem_set.count()
        # if item:
        #     blogs_count=BlogItem.objects.filter(investmentblog=item).count()
        #     return blogs_count
        return 0
    @property
    def has_blogs(self): 
        if  hasattr(self,'investmentblog'):     
            item = self.investmentblog
            if item.blogitem_set:
                if item.blogitem_set.count()>0:
                    return True       
        return False
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
    APLLICATION_STATUS_CHOICE = (("pending", "pending"), ("recieved", "recieved"), 
                               ("verification", "verification"),("accepted", "accepted"),
                                ("engagement", "engagement"),   ("rejected", "rejected") )
    investment = models.ForeignKey(Investment, on_delete=models.SET_NULL, null=True) 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, verbose_name='Keywords')
    motivation = models.TextField(verbose_name='Investment Motivation')
    #postiv float
    value= models.PositiveBigIntegerField(default= 0, verbose_name='Funds Pledge')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    date_status_changed =models.DateTimeField(default=timezone.now())
    application_status = models.CharField(
        choices=APLLICATION_STATUS_CHOICE, max_length=64, default="pending"
    )
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name 
    
    @property
    def time_since_status_updated(self):
        return self.get_time(self.date_status_changed)
    

    def get_time(self,date_in): 
        if date_in ==None:
            date_in  = timezone.now()    
        time_since= timezone.now()- date_in #.split('+')[0]
        if time_since.days>0:
            return str(time_since.days) + str(' days ago')
        elif time_since.days == 0:
            hours = time_since.seconds/3600           
            if hours > 1:
                return str(math.ceil(hours))+ str(' hours ago')
            else:
                minutes = time_since.seconds/60
                if minutes > 1:
                    return str(math.ceil(minutes)) + str(' minutes ago')
                else:
                    return str(time_since.seconds) + str(' seconds ago')
        
        return "Bad Timing"
    
    @property
    def deleted_df(self):
        pass
        #get all that has null investments
    @property
    def trading_df(self):
        #print('gettting')
        
        investments_df = pd.DataFrame(Investment.objects.all().values())
        investors_df = pd.DataFrame(Investor.objects.filter(Q(user=self.user), Q(investment__id__isnull=False)).values())
        
        users_df = pd.DataFrame(User.objects.all().values())
        categories_df = pd.DataFrame(InvestmentCategory.objects.all().values()) 

        df = pd.DataFrame(columns =['iid','retain_id'])
        if investments_df.shape[0]>0 and investors_df.shape[0] > 0 : 
            investments_df['investment_id'] = investments_df['id']
            # mwrge
          
            df =pd.merge(investments_df, investors_df, on='investment_id',how="inner").drop([
                        'likes','views','date_created_y','date_created_x','motivation'
                        ,'name_y','user_id','investment_id'], axis=1).rename(
                        {'id_x': 'iid','id_y': 'retain_id','description':'summary', 'value':'myinvest', 
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
            #print('AL NO>>>>>>>>>>>>>>>>>>>>>>')
            #select only for current user
            return df#[~df['id'].isna()]
        #select only for current user
        #print('#############################################33')
        #print(df.columns)
        df['blogs_count'] = df['iid'].apply(lambda x: self.get_blogs_count(x))
        df['time_since_status_updated'] = df['date_status_changed'].apply(lambda x: self.get_date_status_changed(x))     
         
        return df #[~df['id'].isna()]

    def get_blogs_count(self, id):
        investment_obj= get_object_or_404(Investment, pk=id)
        cnt=investment_obj.blogs_count
        return cnt
    
    def get_date_status_changed(self, date_in):
        return self.get_time(date_in)
       


  
    def trading_df_status(self, application_status=None, slug=None):
        
        if 	slug==None:
            investments_df = pd.DataFrame(Investment.objects.all().values())
        else:
            investments_df = pd.DataFrame(Investment.objects.filter(Q(description__icontains=slug)).values())
        if 	application_status==None:
            investors_df = pd.DataFrame(Investor.objects.filter(Q(user=self.user), Q(investment__id__isnull=False)).values())
        else:
            investors_df = pd.DataFrame(Investor.objects.filter(Q(user=self.user), Q(investment__id__isnull=False), Q(application_status=application_status)).values())
        
        users_df = pd.DataFrame(User.objects.all().values())
        categories_df = pd.DataFrame(InvestmentCategory.objects.all().values()) 

        df = pd.DataFrame(columns =['iid','retain_id'])
        if investments_df.shape[0]>0 and investors_df.shape[0] > 0 : 
            investments_df['investment_id'] = investments_df['id']
            # mwrge
          
            df =pd.merge(investments_df, investors_df, on='investment_id',how="inner").drop([
                        'likes','views','date_created_y','date_created_x','motivation'
                        ,'name_y','user_id','investment_id'], axis=1).rename(
                        {'id_x': 'iid','id_y': 'retain_id','description':'summary', 'value':'myinvest', 
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
            #print('AL NO>>>>>>>>>>>>>>>>>>>>>>')
            #select only for current user
            return df#[~df['id'].isna()]
        #select only for current user
        #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        #print(df.columns)

        df['blogs_count'] = df['iid'].apply(lambda x: self.get_blogs_count(x))
        df['date_status_changed']= pd.to_datetime(df['date_status_changed'])
        df['time_since_status_updated'] = df['date_status_changed'].apply(lambda x: self.get_date_status_changed(x))     
        return df#[~df['id'].isna()]

class Enterprenuer(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name 

