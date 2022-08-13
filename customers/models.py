from django.db import models
from django.contrib.auth.models import User

from store.models import Company, Currency, Product
from django.utils.translation import gettext_lazy as _
import datetime
#delete later
class SalesPlan(models.Model):
    title = models.CharField(max_length=100)
    dstart = models.DateField(null=True)
    dend = models.DateField(null=True)
    status = models.CharField(max_length=10)
    company  = models.ForeignKey(Company, on_delete= models.SET_NULL,null=True)
    currency = models.ForeignKey(Currency, on_delete= models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
    target = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)	
    target_complience = models.CharField(max_length=10, default='below')# below/full/spillover
    note = models.CharField(max_length=500,null=True)
    locked = models.BooleanField(default=False)

class SalesPlanItem(models.Model):
    salesplan = models.ForeignKey(SalesPlan, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE,null=True) 
    # Saleaplan useless if no product
    period = models.CharField(max_length=10, null=True)# H1,H2, Q1, Q2,Q3,Q4,M1,M2....M12, W1---W52,D1---D365
    dstart = models.DateField(null=True)
    dend = models.DateField(null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10)# reduntant
    qty = models.IntegerField()
    date_created =models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
class Employee(models.Model):
    MSTATUS = (       
        ('Married', 'Married'),
        ('Single', 'Single'),
        ('Divorced', 'Divorced'),
        ('Anonymous', 'Anonymous'),
    )

    MGENDER = (       
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Anonymous', 'Anonymous'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    basic_salary = models.IntegerField(default=10000, blank=True, null=True)
    bonus = models.FloatField(default=0, blank=True, null=True)
    grade = models.CharField(max_length=15, default="")
    gender = models.CharField(max_length=10, choices= MGENDER, default='Male')
    start_date = models.DateField(verbose_name='Service Entry Date', default=datetime.datetime(2018,1,1))
    marital_status = models.CharField(max_length=10, choices=MSTATUS, default='Married')
    dob = models.DateField(default=datetime.datetime(2000,1,1))
    nationality = models.CharField(max_length=20,null=True,blank=True, default='Zimbabwean')
    telephone_no = models.CharField(max_length=20, null=True,blank=True)
    residence_address = models.CharField(max_length=50, null=True,blank=True)
    national_id = models.CharField(max_length=20,null=True,blank=True)
    annual_allowance = models.IntegerField(default=21)
    image_url = models.CharField(max_length=20,null=True, default="")
    status = models.CharField(max_length=20, default="Active")
    title = models.CharField(max_length=10, blank=True, default ='Mr.')
    work_station = models.CharField(max_length=20, null=True,blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True,blank=True)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name

class CompanyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # no duplicates allowed here
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    company = models.ManyToManyField(Company, blank=True, null=True)
   
    class Meta:
        verbose_name = _("Company User")
        verbose_name_plural = _("Company Users")

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name

    def get_companies(self):
        return ",".join(
            [str(_id) for _id in list(self.company.values_list("id", flat=True))]
        )

    def get_mpds(self):
        return ",".join(
            [str(_id) for _id in list(self.mpd.values_list("id", flat=True))]
        )
    def get_workshops(self):
        return ",".join(
            [str(_id) for _id in list(self.workshop.values_list("id", flat=True))]
        )

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

