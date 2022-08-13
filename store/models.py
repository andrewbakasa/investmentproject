
from __future__ import unicode_literals
from django.db import models

from django.dispatch import receiver

from django.db.models.signals import post_save

from django.contrib.auth.models import  Group #User,
from django.conf.urls.static import static
from common.models import User


from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
#from common.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date



class ClientCompany(models.Model):
	
	#user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	user = models.ManyToManyField(User, blank =True)
	name = models.CharField(max_length=200, null=True )
	address1 = models.CharField(max_length=500, null=True, blank=True)
	address2 = models.CharField(max_length=256,null=True, blank=True)
	phone = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=128, null=True, blank=True)
	state = models.CharField(max_length=50, null=True, blank=True)
	zip = models.CharField(max_length=12, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	rating = models.IntegerField(default=0)
	locked = models.BooleanField(default=False)
	# to change a company to have multiple users for reports sharing...


	def invoices(self):
			return Invoice.objects.filter(customer=self).count()

	def __str__(self):
		if self.name:
			return self.name
		else :
			return "No name"	

class ClientReportAttachmentQuerySet(models.QuerySet):
    def by_client(self,cust):
        return self.filter(customer=cust).order_by('-date')

    def date_range(self, dstart, dend):
        return self.filter(date__gte=dstart, date__lte=dend)

    def by_client_date_range(self, cust, dstart, dend):
        return self.self.filter(customer=cust).filter(date__gte=dstart, date__lte=dend)


    def upcoming(self):
        return self.filter(date__gt=date.today())

    def past(self):
        return self.filter(date__lte=date.today())

# Create your models here.
class ClientReportAttachment(models.Model):
    file = models.FileField(upload_to='clientreports/')
    displayname = models.CharField(max_length=128)
    customer = models.ForeignKey(ClientCompany, on_delete=models.CASCADE, null=True)
    periodname = models.CharField(max_length=128, default="not-available")
    date = models.DateField(default=date.today)
    last_modified = models.DateTimeField(auto_now=True)
    locked = models.BooleanField(default=True)

    class Meta:
            ordering = ['-date']

    def __str__(self):
        if self.displayname:
            return self.displayname + " for {" + str(self.customer) + "}"
        else :
            return "No name"

    objects = ClientReportAttachmentQuerySet.as_manager()	
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


# Create your models here.
class Customer(models.Model):
	# one user to many customer 0ne-to-many......
	# in future have onetoone..... Each user to have only one customer account
	#user = models.ForeignKey(User, null=True, blank=True, on_delete= models.SET_NULL)
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	#user = models.ManyToManyField(User, null=True, blank =True)
	coporateclient =models.BooleanField(verbose_name="businessclient", default=False)
	# user = models.OneToOneField(User, null=True, blank=True, on_delete= models.SET_NULL)
	name = models.CharField(max_length=200, null=True )
	address1 = models.CharField(max_length=500, null=True, blank=True)
	address2 = models.CharField(max_length=256,null=True, blank=True)
	phone = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=128, null=True, blank=True)
	state = models.CharField(max_length=50, null=True, blank=True)
	zip = models.CharField(max_length=12, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	rating = models.IntegerField(default=0)
	locked = models.BooleanField(default=False)
	# to change a company to have multiple users for reports sharing...


	def invoices(self):
			return Invoice.objects.filter(customer=self).count()

	def __str__(self):
		if self.name:
			return self.name
		else :
			return "No name"	

		
class InvoiceQuerySet(models.QuerySet):
    def last_10(self):
        return self.order_by('-date')[:10]
   
    def date_range(self, dstart, dend):
        # filter or
        return self.filter(date__gte=dstart, date__lte=dend)
  
    def upcoming(self):
        return self.filter(date__gt=date.today())

    def past(self):
        return self.filter(date__lte=date.today())

class Invoice(models.Model):
	number = models.IntegerField(verbose_name=_("invoice_number"))	
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name="Contact Person")
	clientcompany = models.ForeignKey('ClientCompany', on_delete=models.SET_NULL,null=True, verbose_name="Client Company")
	parentorder = models.OneToOneField('Order', on_delete=models.SET_NULL,null=True)
	date = models.DateField()
	status = models.CharField(max_length=10)
	company  = models.ForeignKey(Company, on_delete= models.SET_NULL,null=True, verbose_name="Service Provider")
	currency = models.ForeignKey('Currency', on_delete= models.SET_NULL, null=True)
	locked = models.BooleanField(default=False)

	def __str__(self):
		return str(self.number)

	def total_items(self):
		total = 0
		items = self.invoiceitem_set.all()

		for item in items:
			total += item.cost * item.qty

		return total

	def total_expenses(self):
		total = 0
		expenses = self.expense_set.all()

		for expense in expenses:
			total += expense.cost * expense.qty

		return total

	def total(self):
		items = self.total_items()
		expenses = self.total_expenses()

		return float(items - expenses)
		
	def paid(self):
		return self.status == 'Paid'
		
	def unpaid(self):
		return self.status == 'Unpaid'
		
	def draft(self):
		return self.status == 'Draft'

	def has_children(self):
		return self.invoiceitem_set.count() > 0

	objects = InvoiceQuerySet.as_manager()		

class InvoiceItem(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	product = models.ForeignKey('Product', on_delete= models.SET_NULL,null=True)
	# name = models.CharField(max_length=128)
	# description = models.TextField()
	cost = models.DecimalField(decimal_places=2, max_digits=10)
	qty = models.IntegerField()

	def total(self):
		return float(self.cost * self.qty)

	class Meta:
		ordering = ['product']
		unique_together = (('product', 'invoice'),)


class Expense(models.Model):
	description = models.TextField()
	cost = models.DecimalField(decimal_places=2, max_digits=10)
	qty = models.IntegerField()
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateField(default=date.today)
	company  = models.ForeignKey(Company, on_delete= models.SET_NULL,null=True)
	currency = models.ForeignKey("Currency", on_delete= models.SET_NULL, blank=True, null=True)
		
	def total(self):
		return self.cost * self.qty

	def is_business_expense(self):
		return self.invoice is None

class InvoiceAttachment(models.Model):
	file = models.FileField(upload_to='invoice/')
	displayname = models.CharField(max_length=128)
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

class ExpenseAttachment(models.Model):
	file = models.FileField(upload_to='expense/')
	displayname = models.CharField(max_length=128)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE)



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





@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        #----- create group for this use ----------------------
        group, created_new = Group.objects.get_or_create(name ='customer')
        #group = Group.objects.get(name ='customer')
        instance.groups.add(group)

        Customer.objects.get_or_create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
        #-----------------------------------


class ProductCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(default=16383)
    
    # image
    image = models.ImageField(upload_to='category_images', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['priority','name']

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url ="" 

        return url

    class Meta:
        verbose_name_plural = "ProductCategories"


class Product(models.Model):
    name = models.CharField('category', max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
    company  = models.ManyToManyField(Company, blank=True)
    priority = models.PositiveSmallIntegerField(default=16383)
    # Image
    image = models.ImageField(upload_to='product_images', blank=True)

    # divisions
    categories = models.ManyToManyField(ProductCategory,verbose_name="divisions")
    
    locked = models.BooleanField(default=False)

    def get_priority(self):
        min_val=16383

        for cat in self.categories.all():
            if cat.priority:
                if min_val > cat.priority:
                    min_val=cat.priority
        return min_val

    def save(self, *args, **kwargs):
        #---need an id to ensure many-to-many-is accesible
        if not self.id:
            super(Product, self).save(*args, **kwargs)
        #then can be able to access already saved id
        self.priority= self.get_priority()
        super(Product, self).save(*args, **kwargs)
        # was reocrding error...
   

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['priority','name']

    @property
    def imageURL(self):
        try:
            url = self.image.url
          
        except:
            url = "" 
      
        return url

# represents cart
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    company  = models.ForeignKey(Company, on_delete= models.SET_NULL,null=True, blank=True)
    currency = models.ForeignKey("Currency", on_delete= models.SET_NULL, null=True, blank=True)

    locked = models.BooleanField(default=False)

    def __str__(self):
        # some orders dont have customers
        # 19 Feb 2022
        # fix all scenario when this migh occur
        return str(self.customer.name if self.customer  else "" + " " + str(self.id))

    class Meta:
        ordering = ['-date_ordered']
    # get total price
    # of all items
    # in the order or cart
    @property
    def total_price(self):
        orderitems = self.orderitem_set.all()
        totalprice = sum([orderitem.total for orderitem in orderitems])
        return float(totalprice)

    # get total amount
    # of all items
    # in the order or cart
    @property
    def total_quantity(self):
        orderitems = self.orderitem_set.all()
        totalquantity = sum([orderitem.quantity for orderitem in orderitems])
        return totalquantity

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.product.digital == False:
                shipping = True
        return shipping

class OrderAttachment(models.Model):
    file = models.FileField(upload_to='order/')
    displayname = models.CharField(max_length=128)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        total_val= 0
        #---some products have null value: 
        # This is caused when a product field is set to  None after related product is deleted
        # or when an order is created without items
        #---error corrected Heroku thru error 06 March 2021
        if self.product != None:
            price_per_item = self.product.price
            total_val = price_per_item * self.quantity

        return total_val

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


