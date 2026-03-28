from __future__ import unicode_literals
import datetime
import math
from os import access

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
#from common.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date
# from store.models import Currency
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.core.validators import RegexValidator


# 1. Define the validator outside the class
id_regex = RegexValidator(
    regex=r'^[a-z0-9]+$', 
    message="ID must be lowercase letters and numbers only (e.g., fish001). No spaces, dashes, or symbols."
)

def get_curr_year():
    current_year = datetime.datetime.now().year
    return int(current_year)

class SimulationParameters(models.Model):
    max_simulation_iter = models.IntegerField(default=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.date_created)
class NewsSubscribe(models.Model):
    email = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.email 
class Downloads(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Model Owner")
    model_type = models.ForeignKey('ModelCategory', on_delete=models.SET_NULL, null=True,verbose_name="Category")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.user.username if self.user else self.model_type.name

class Events(models.Model):

    PRODUCT_LAUNCH = 1
    SYSTEM_UPGRADE = 2
    ANOUNCEMENT = 3
    EVENT_TYPES = (
        (PRODUCT_LAUNCH, _('PRODUCT_LAUNCH')),
        (SYSTEM_UPGRADE, _('SYSTEM_UPGRADE')),
        (ANOUNCEMENT, _('ANOUNCEMENT')),
    )

   
    title = models.CharField(max_length=200, null=True )
    event_type = models.IntegerField(choices=EVENT_TYPES, default=PRODUCT_LAUNCH)
    accessible= models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title 
   

class PurchasePlan(models.Model):
    name = models.CharField(max_length=200, null=True )
    email = models.CharField(max_length=200, null=True, blank=True)
    userplan = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.userplan} : {self.email}'     
class ContactUs(models.Model):
    name = models.CharField(max_length=200, null=True )
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.subject 
    
    @property
    def time_since_created(self):
        return self.get_time(self.date_created)
    

    def get_time(self,date_in):        
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
class Company(models.Model):
	name = models.CharField(max_length=200, null=True )
	street = models.CharField(max_length=500, null=True, blank=True)
	city = models.CharField(max_length=256,null=True, blank=True)
	country = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	zip = models.CharField(max_length=12, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)	
	locked = models.BooleanField(default=False)

	class Meta:
		verbose_name = _("Company List")
		verbose_name_plural = _("Company List")

	def __str__(self):
		return self.name 
	
class Currency(models.Model):
	name = models.CharField(max_length=50,unique=True, default="United States Dollar")
	symbol = models.CharField(max_length=50,default="USD")
	country = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	@property
	def current_rate(self):
		return self.current_rate_on(date.today())

	@property
	def rate_on(self, dstart):
		return self.current_rate(dstart)

	def current_rate_on(self, date):
		c_rate = CurrencyRate.objects.filter(currency=self, date__lte=date).order_by('-date').first()
		if c_rate:
			return	c_rate.rate
	
		return 1 # default rate if none is given




	# currency = models.Currency.objects.get(pk=self.account)

	# currency.current_rate
	# currency.rate_on('20/10/2020')

class CurrencyRateQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('-date')[:10]
   
    def date_range(self, dstart, dend):
        # filter or
        return self.filter(date__gte=dstart, date__lte=dend)

    def active(self):
        return self.filter(active=True)
    
    def upcoming(self):
        return self.filter(date__gt=date.today())

    def past(self):
        return self.filter(date__lte=date.today())

class CurrencyRate(models.Model):
	currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
	date = models.DateField()
	rate = models.DecimalField(decimal_places=2, max_digits=10)

	# def __str__(self):
	# 	return self.rate.

	class Meta:
		ordering = ['-date']

	objects = CurrencyRateQuerySet.as_manager()	
class UserModelQuerySet(models.QuerySet):
    def last_10(self):
        pass
   
    def date_range(self, dstart, dend):
        pass
  
    def upcoming(self):
        pass

    def past(self):
        pass

class ModelCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    
    # 2. Apply the validator and the descriptive help_text
    uniqueid = models.CharField(
        max_length=200, 
        unique=True,
        validators=[id_regex],
        help_text="Format: [app_name][number]. Examples: **fish001**, **beef011**, **greenhouse008**. "
                  "This MUST match the exact folder name in your templates directory."
    )
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
        
    class Meta:
        ordering = ['-hits']
    
    @property
    def app_folder(self):
        # 1. Strip all numbers from the right side of the string
        # 2. Add 'app' to the end
        # Example: 'greenhouse008' -> 'greenhouse' + 'app' = 'greenhouseapp'
        clean_name = self.uniqueid.rstrip('0123456789')
        return f"{clean_name}app"
    def __str__(self):
        return str(self.name)

    # 3. Add the save method to 'Auto-Fix' common admin mistakes
    def save(self, *args, **kwargs):
        if self.uniqueid:
            # Force lowercase and remove all whitespace/dashes before saving
            self.uniqueid = self.uniqueid.lower().strip().replace(" ", "").replace("-", "")
        super(ModelCategory, self).save(*args, **kwargs)
    
    @property
    def details(self):
        # Using getattr to prevent a crash if modelcategorydetails doesn't exist
        item = getattr(self, 'modelcategorydetails', None)
        dict_ = {}
        if item:
            dict_['head'] = item.head if item.head else ""
            dict_['sector'] = item.sector if item.sector else ""
            dict_['premium'] = item.premium
            dict_['motto'] = item.motto if item.motto else ""
        return dict_



class ModelCategoryDetails(models.Model):
    category = models.OneToOneField(ModelCategory, on_delete=models.CASCADE)
    head = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
    sector = models.TextField()
    motto = models.TextField(blank=True,null=True)
    premium = models.BooleanField(default=False) 
    date_created = models.DateTimeField(auto_now_add=True, null=True)
   	
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.category)  
class UserModel(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Model Owner")
    model_type = models.ForeignKey(ModelCategory, on_delete=models.SET_NULL, null=True,verbose_name="Category")
    name = models.CharField(verbose_name=_("Model Title"), max_length=200, null=False )
    description = models.TextField(default='My own model')	
    status = models.CharField(max_length=20, default='WIP')
    currency = models.ForeignKey(Currency, on_delete= models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True,null=True)
    locked = models.BooleanField(default=False)
    simulation_iterations =models.IntegerField(default=100)
    simulation_run =models.BooleanField(default=False)
    npv_bin_size= models.IntegerField(default=10)
    design_complete =models.BooleanField(default=False)
    total_params= models.IntegerField(default=0, verbose_name="Simulation Params")
    hits = models.IntegerField(default=0)# downloads


    @property
    def app_folder(self):
    # Check if model_type exists and get its uniqueid string
        if self.model_type and hasattr(self.model_type, 'uniqueid'):
            # We call rstrip on the STRING 'uniqueid', not the object itself
            clean_name = self.model_type.uniqueid.rstrip('0123456789')
            return f"{clean_name}app"
        return "defaultapp" # Fallback if something is missing
    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-last_modified','-date_created']
        unique_together = (('user', 'name'),)

    def __str__(self):
        return str(self.name)


    def unpaid(self):
        return self.status == 'Unpaid'
        
    def draft(self):
        return self.status == 'Draft'

    def model_fully_specified(self):
        if self.model_type == UserModel.CATTLEFATTENNING:
            ta= self.timingAssumption_set.count() > 0
            p= self.prices.count() > 0
            d= self.depreciation_set.count() > 0
            f= self.financing.count() > 0
            return (ta and p and d and f)
        return False   

    objects = UserModelQuerySet.as_manager()		


 

class InvestmentOptions(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    #two dimension
    optionparameters = ArrayField(
        ArrayField(
            models.DecimalField(decimal_places=2, max_digits=10, default =1000),
            size=6,
        ),
        size=11,
    )

    class Meta:
        ordering = ['usermodel']
        #unique_together = (('product', 'invoice'),)    
class TimingAssumption(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    base_period = models.IntegerField(default =get_curr_year())
    construction_start_year =  models.IntegerField(default =get_curr_year())
    construction_len =  models.IntegerField(default =1)
    construction_year_end = models.IntegerField(default =get_curr_year())
    operation_start_year =  models.IntegerField(default =get_curr_year()+1)
    operation_duration = models.IntegerField(default =10)
    operation_end = models.IntegerField(default =get_curr_year() + 10-1)
    number_of_months_in_a_year = models.IntegerField(default =12)


    class Meta:
        ordering = ['usermodel']
        #unique_together = (('product', 'invoice'),)
    
    def __str__(self):
        return str(self.usermodel)
class Prices(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default ='Base_Price')
    base_price = models.DecimalField(decimal_places=2, max_digits=10, default =3500)
    change_in_price = models.DecimalField(decimal_places=2, max_digits=10, default =.0)

    class Meta:
        ordering = ['usermodel']
        #unique_together = (('product', 'invoice'),)

class Depreciation(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    economic_life_of_machinery =  models.IntegerField(default =20)
    economic_life_of_buildings =  models.IntegerField(default =30)
    tax_life_of_machinery =  models.IntegerField(default =10)
    tax_life_of_buildings =  models.IntegerField(default =10)
    tax_life_of_soft_capital_costs =  models.IntegerField(default =3)

    class Meta:
        ordering = ['usermodel']
        #unique_together = (('product', 'invoice'),)


class Financing(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    real_interest_rate =  models.DecimalField(default =.05, decimal_places=2, max_digits=10)
    risk_premium =  models.DecimalField(default =.01, decimal_places=2, max_digits=10)
    num_of_installments =  models.IntegerField(default =6)
    grace_period =  models.IntegerField(default =1)
    #repayment_starts =  models.IntegerField(default = get_curr_year()+1)
    equity =  models.DecimalField(default =.3, decimal_places=2, max_digits=10)
    senior_debt =  models.DecimalField(default =.7,decimal_places=2, max_digits=10)
    
    class Meta:
        ordering = ['usermodel']
        #unique_together = (('product', 'invoice'),)

class WorkingCapital(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    accounts_receivable =  models.DecimalField(decimal_places=2, max_digits=10, default=.1)
    accounts_payable =  models.DecimalField(decimal_places=2, max_digits=10, default=.1)
    cash_balance =  models.DecimalField(decimal_places=2, max_digits=10, default=.1)
   
    class Meta:
        ordering = ['usermodel']
        #unique_together = (('product', 'invoice'),)

class Taxes(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    import_duty =  models.DecimalField(decimal_places=2, max_digits=10, default =.1)
    sales_tax =  models.DecimalField(decimal_places=2, max_digits=10, default =.25)
    corporate_income_tax =  models.DecimalField(decimal_places=2, max_digits=10,default =.05)
 

class MacroeconomicParameters(models.Model):
    usermodel = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    discount_rate_equity =  models.DecimalField(decimal_places=2, max_digits=10, default=.12)
    domestic_inflation_rate =  models.DecimalField(decimal_places=2, max_digits=10,default=.1)
    us_inflation_rate =  models.DecimalField(decimal_places=2, max_digits=10, default=.03)
    exchange_rate =  models.DecimalField(decimal_places=2, max_digits=10, default=1)
    dividend_payout_ratio =  models.DecimalField(decimal_places=2, max_digits=10, default=.25)
    num_of_shares =  models.IntegerField(default=0)
    investment_costs_over_run_factor =  models.DecimalField(decimal_places=2, max_digits=10, default=0)
   
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    perpage_blogs = models.IntegerField(default=6, verbose_name='Blogs Page Records')
    perpage = models.IntegerField(default=6, verbose_name='Page Records')
    pertable = models.IntegerField(default=10, verbose_name='Table Records')
    g2 = models.BooleanField(default=True, verbose_name='G2: another')
  
    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['last_modified',] 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    age = models.IntegerField(default=18)
    country = models.CharField(max_length=200, blank=True, null=True)
    sex = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True) 
    aboutyou = models.TextField(blank=True, null=True, verbose_name='About Me') 
    last_login= models.DateTimeField(blank=True, null=True)
    login_count=models.IntegerField(default=0)
    
    # Image
    image = models.ImageField(upload_to='profile_images', blank=True)

  
    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['last_modified',]         
    
       
    @property
    def imageURL(self):
        try:
            url = self.image.url
          
        except:
            url = "" 
      
        return url