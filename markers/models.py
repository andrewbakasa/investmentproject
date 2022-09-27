from pyexpat import model
from django.contrib.gis.db.models import PointField
from django.db import models
from django.contrib.auth.models import User

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
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
  

    def __str__(self):
        if self.description:
            return self.description
        return "No Data"
    
    class Meta:
        ordering = ['date_created']
    @property
    def get_target(self):
        l =''
        items = self.targetA.all()
        for item in items:
            if l=="" and item.target:
                l = str(item.target.created_by.username)
            elif item.target:
                l += ',' + str(item.target.created_by.username)

        return l
    @property    
    def get_source(self):
        l =''
        items = self.targetA.all()#.source
        for item in items:
            if l=="" and item.source:
                l = str(item.source.created_by.username)
            elif item.source:
                l = l + ',' + str(item.source.created_by.username)
        return l
class CurrencyTag(models.Model):
    target = models.ForeignKey(TradedCurrency,related_name="targetA", on_delete= models.SET_NULL, null=True)
    source = models.ForeignKey(TradedCurrency,related_name="sourceA", on_delete= models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified=models.DateTimeField(auto_now=True)
    #tagged  =models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
    def __str__(self):
        if self.created_by:
            return self.created_by.username
        return "No Data"
    
    class Meta:
        ordering = ['date_created']

    
from django.contrib.gis.db import models as gis_models

