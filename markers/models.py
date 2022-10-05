from email.policy import default
from pyexpat import model
from django.contrib.gis.db.models import PointField
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.contrib.gis import forms

from django.contrib.gis.db import models as geo_models

from store.models import Currency

class Marker(models.Model):
    name = models.CharField(max_length=255)
    location = PointField(default=None)#see far way country.....

class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    location = PointField(default=None)
    
    def __str__(self):
        if self.user:
            return self.user.username
        else :
            return "No name"
    
    # def get_absolute_url(self):
    #     return reverse('shop-update', kwargs={'pk':self.pk})

    class Meta:
        ordering = ['location']


class TradedCurrency(models.Model):
    #user = models.ForeignKey(User, null=True, blank=True, on_delete= models.SET_NULL)
    residence = models.ForeignKey(UserLocation,verbose_name="location", related_name='residenceA', on_delete= models.SET_NULL,null=True, blank=False)
    currency_offered =models.ForeignKey(Currency, related_name="offered", on_delete= models.SET_NULL, null=True)
    currency_expected = models.ForeignKey(Currency,related_name="expected", on_delete= models.SET_NULL, null=True)
    rate_expected = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    value = models.IntegerField(verbose_name="Offered Value",default=0)
    complete =models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
  

    def __str__(self):
        if self.created_by:
            return self.created_by.username
        return "No Data"
    
    class Meta:
        ordering = ['date_created']
    
    @property    
    def get_matching_partner(self):
      
        items = self.targetA.all()#.s
        if items:
            return items.first().matching_partner()
        return False
    @property    
    def get_already_matched(self):
      
        items = self.targetA.all()#.s
        if items:
            return items.first().already_matched()
        return False
        
    @property    
    def get_suitor(self):
        #get all tags created by this user
        qs= CurrencyTag.objects.filter(Q(source__created_by =self.created_by))#.exclude(Q(source__created_by=self.created_by))
        if qs:
            l =""
            for i in qs:
                #get the username list
                if l=="":
                    l= i.target.created_by.username
                else:
                    l= l + "," + i.target.created_by.username

            return l + ","
        return ""
    @property    
    def get_source_target(self):
        l =''
        l_twin =""
        items = self.targetA.all()#.source
       
        for item in items:
            if item.source:
                if l =="":
                    l = str(item.source.created_by.username)
                else:
                    l = l + ',' + str(item.source.created_by.username)
            if item.target:
                if l_twin =="":
                    l_twin = str(item.target.created_by.username)
                else:
                    l_twin = l_twin + ',' + str(item.target.created_by.username)
        #print('Source', items, l,l_twin)
        return l + "," + l_twin
    @property
    def get_target(self):
        l =''
        l_twin=""
        items = self.targetA.all()
        # g =""
        # for i in items:
        #     g += i.target.created_by
        for item in items:
            if l=="" and item.target:
                l = str(item.target.created_by.username)
                l_twin = str(item.source.created_by.username)
            else:
               if item.target:
                    i += ',' + str(item.target.created_by.username)
               if item.source:
                    l_twin += ',' + str(item.source.created_by.username)
        print('Target', items,l, l_twin)
        return l
    @property    
    def get_source(self):
        l =''
        l_twin =""
        items = self.targetA.all()#.source
        # g =""
        # for i in items:
        #     g+= i.source.created_by

        
        for item in items:
            if l=="" and item.source:
                l = str(item.source.created_by.username)
                l_twin =str(item.target.created_by.username)
            else :
                if item.source:
                    l = l + ',' + str(item.source.created_by.username)
                if item.target:
                    l_twin = l_twin + ',' + str(item.target.created_by.username)
        print('Source', items, l,l_twin)
        return l
class CurrencyTag(models.Model):
    target = models.ForeignKey(TradedCurrency,related_name="targetA", on_delete= models.CASCADE, null=True)
    source = models.ForeignKey(TradedCurrency,related_name="sourceA", on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified=models.DateTimeField(auto_now=True)
    #tagged  =models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    def __str__(self):
        if self.created_by:
            return self.created_by.username
        return "No Data"
    
    class Meta:
        ordering = ['date_created']

    def matching_partner(self):
        qs= CurrencyTag.objects.filter(Q(source=self.target), Q(target =self.source))
        if qs:
            return True
        return False
    
    def already_matched(self):
        #fetch all sources that terminate with me
        # is this targeget
        #for all other check if their target point to source
        qs= CurrencyTag.objects.filter(Q(target =self.source))
        if qs:
            return True
        return False

        

class NearbyDistance(models.Model):
    source = models.OneToOneField(TradedCurrency,related_name="nearbyA", on_delete= models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified=models.DateTimeField(auto_now=True)
    distance= models.IntegerField(default=1000)
    def __str__(self):
        if self.date_created:
            return str(self.date_created)
        return "No Data"
    
    class Meta:
        ordering = ['date_created']
