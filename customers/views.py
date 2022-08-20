from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group
from common.utils import get_current_user_groups
from investments_appraisal.models import UserPreference

from store.decorators import unauthenticated_user, allowed_users, admin_only, registered_user_only_with_client_routing


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
from store.models import *
from .forms import OrderForm, CreateUserForm, ProductForm, CustomerForm, ExportForm, ProductUpdateForm
#from .models import ClientCompany
from .filters import OrderFilter, CustomerFilter

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.forms.models import model_to_dict
import decimal

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils.decorators import method_decorator

from store.models import Customer, Currency, Company
import datetime

from django.views import generic

#from store.lib import get_current_user_groups
from itertools import chain
from store.models import Order, OrderItem,  OrderAttachment
from .models import SalesPlanItem
from datetime import date
from silverstrike.lib import last_day_of_month, short_month_name
import csv
from dateutil.relativedelta import relativedelta
from store.models import Invoice, InvoiceItem, Expense



from customers.models import CompanyUser
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from store.models import Invoice

from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.conf import settings
from django.db.models.aggregates import Avg, Count, Max, Sum
from django.db.models import Q

 
from django.utils import timezone


login_required(login_url="account_login")
def show_address(request,pk):
    address = ShippingAddress.objects.filter(order__id=pk).first()
    address = ShippingAddress.objects.filter(order__id=pk).first()
    print(address)
    return save_all2(request,address,'customers/show_address_modal.html')

def save_all2(request,address,template_name):
    data = dict()
    
    context = {
    'address':address
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    #print(data)
    return JsonResponse(data)


login_required(login_url="account_login")
def create_userproduct_ajax(request):
	if request.method == 'POST':
		form = ProductForm(request.POST or None, request.FILES or None)
	else:
		#first time call from loco failure list
		form = ProductForm(initial={'created_by': request.user})
	return create_all_user_product(request,form,'customers/user_product_modal.html')


login_required(login_url="account_login")
def create_all_user_product(request,form,template_name):

    data = dict()
    errors= None
    if request.method == 'POST':
        errors=form.errors
        
        if form.is_valid():
            form.save()
            #form.us
            data['form_is_valid'] = True
            latest = Product.objects.latest('id').id
            record = Product.objects.get(pk=latest)
            item_object = model_to_dict(record)
            print(item_object)
            #categories = []
            # for j in record.categories.all():
            #     categories.append(j.name)
            # item_object['categories']= categories
            categories=""
            for x in item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            item_object['categories']=  categories[:len(categories)-2]
            if record.image:
                item_object['image']= record.image.url
            else:
                item_object['image']=None
            data['model'] = item_object
        else:
            data['form_is_valid'] = False
            # print('nofield errors: ',form.non_field_errors)
            # print('errors:::',form.errors)
    context = {
        'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    data['error']=errors
    return JsonResponse(data)



@login_required(login_url="account_login")
def get_user_products(request, type):
    BUSINESS_STATUS_CHOICE = ["all"]#["unread","open","closed","all"] 
    current_time =timezone.now()# datetime.datetime.now()
      

   
    queryset = Product.objects.filter(Q(created_by=request.user))
    
    
    total_avg= queryset.aggregate(sum=Sum('price'), avg=Avg('price'))
    sum_value=total_avg['sum']
    avg_value=total_avg['avg']
    if sum_value==None:
        sum_value=0
    if avg_value==None:
        avg_value=0  
    form = ProductForm(initial={'created_by': request.user})
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    else:
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    pertable=request.session['pertable']
    obj_paginator = Paginator(queryset, pertable)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'current_page':current_page,
        'page_range':page_range,
        "user": request.user,
        "models": queryset,
        "total": queryset.count(),
        "user": request.user,
        'form': form,
         'status': type,
        "BUSINESS_STATUS_CHOICE": BUSINESS_STATUS_CHOICE,
        "total_sum": float(round(sum_value,2)),
        "average": round(avg_value,2),
        'lock_key':True,
        'edit_key':True
    }
   
    return render(request, 'customers/user_products.html', context)

def display_toggle_order_ajax(request, id):
    current_time = timezone.now()#datetime.datetime.now()
    
    userdata= get_object_or_404(OrderItem,pk=id)

    status=""
    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None)
        print(userdata)
        if userdata.fullfilled:
            userdata.fullfilled =False
            userdata.save()
            status= 'Pending'
        else:
            userdata.fullfilled =True
            userdata.save()
            status= 'FullFilled'
         
        data={}	
        data["changed"]=True
        data["status"]=status
      

        return JsonResponse({"data":data})
def display_userproduct_ajax(request):
    current_time = timezone.now()#datetime.datetime.now()
    
    userdata= Product.objects.filter(created_by=request.user)

    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 3
    pertable=request.session['pertable']
    obj_paginator = Paginator(userdata, pertable)
    first_page = obj_paginator.page(1).object_list
    page_range = obj_paginator.page_range
    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None)
        #print('page:', page_no) 
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
        current_page = obj_paginator.get_page(page_no)   
        data={}	
        data["per_table"]=pertable
        data["page_no"]=page_no
        data["num_of_pages"]=num_of_pages
        data["totalrecords"]=totalrecords
        
        #data["has_previous"]=False
        if current_page.has_previous():
            data["has_previous"]=True  
            data["first"]=1 
            data["previous_page_number"]=current_page.previous_page_number() 
        
        data["current_page"]=current_page.number     
        
        #data["has_next"]=False
        if current_page.has_next():
            data["has_next"]=True  
            data["next_page_number"]=current_page.next_page_number()
        
        data["last"]=current_page.paginator.num_pages 
        if int(page_no)>int(num_of_pages):			
            data["results"]=[]
            return JsonResponse({"data":data})

                                                
        results=[] 												 
        for i in obj_paginator.page(page_no).object_list:

            item_object = model_to_dict(i)
           
            categories=""
            for x in item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            item_object['categories']=  categories[:len(categories)-2]
            if i.image:
                item_object['image']= i.image.url
            else:
                item_object['image']=None
           
            results.append(item_object)
		
        data["results"]=results
        return JsonResponse({"data":data})

def display_user_clients_ajax(request):
    # class OrderItem(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    # quantity = models.IntegerField(default=0, null=True, blank=True)
    # date_added = models.DateTimeField(auto_now_add=True)

    # @property
    # def total(self):
    #     total_val= 0
    #my_clients------
    userdata= OrderItem.objects.filter(product__created_by=request.user).order_by('-order__id').order_by('-order__date_ordered')
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 3
    pertable=request.session['pertable']
    obj_paginator = Paginator(userdata, pertable)
    first_page = obj_paginator.page(1).object_list
    page_range = obj_paginator.page_range
    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None)
        #print('page:', page_no) 
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
        current_page = obj_paginator.get_page(page_no)   
        data={}	
        data["per_table"]=pertable
        data["page_no"]=page_no
        data["num_of_pages"]=num_of_pages
        data["totalrecords"]=totalrecords
        
        #data["has_previous"]=False
        if current_page.has_previous():
            data["has_previous"]=True  
            data["first"]=1 
            data["previous_page_number"]=current_page.previous_page_number() 
        
        data["current_page"]=current_page.number     
        
        #data["has_next"]=False
        if current_page.has_next():
            data["has_next"]=True  
            data["next_page_number"]=current_page.next_page_number()
        
        data["last"]=current_page.paginator.num_pages 
        if int(page_no)>int(num_of_pages):			
            data["results"]=[]
            return JsonResponse({"data":data})

                                                
        results=[] 												 
        for i in obj_paginator.page(page_no).object_list:

            item_object = model_to_dict(i)
            #print (type(i.customer.details))
            if i.order:
                if isinstance(i.order.customer.details, User):
                        item_object['customer_details']=i.order.customer.details.username
                else:
                    item_object['customer_details']= i.order.customer.details
            else:
                item_object['customer_details'] =None 

            item_object['date_added']=i.date_added.ctime()

            if i.order:
                item_object['on']= i.order.id
                if i.order.currency:
                    item_object['currency_symbol']= i.order.currency.symbol
                else:
                    item_object['currency_symbol']= '$'
            else:
                item_object['currency_symbol']= '$'
                item_object['on']= None

            
            item_object['total']= i.total
            if i.product:
                item_object['price']= i.product.price
                item_object['prn']= i.product.id
                item_object['product']= i.product.name
            else:
                item_object['price']=None
                item_object['prn']=None
                item_object['product']= None

                                   
           
            results.append(item_object)
		
        data["results"]=results
        return JsonResponse({"data":data})

def get_user_clients_load_status_ajax(request,  status, *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            BUSINESS_STATUS_CHOICE = ["wip","ready","fullfilled", 'all']
            current_time = timezone.now()#datetime.datetime.now() 
            bus_status = request.POST.get('bus_status', None)
            #Paging click
            if bus_status != None:
                status=bus_status

            if status =="wip":
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=False)).order_by('-order__id').order_by('-order__date_ordered')

            elif status =="ready": 
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=True),Q(fullfilled=False)).order_by('-order__id').order_by('-order__date_ordered')

            elif status =="fullfilled":
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(fullfilled=True)).order_by('-order__id').order_by('-order__date_ordered')

            else:
                #allll
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user)).order_by('-order__id').order_by('-order__date_ordered')
        
            avg_value=0 
            sum_value=0
            # total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
            # sum_value=total_avg['sum']
            # avg_value=total_avg['avg']
            if sum_value==None:
                sum_value=0
            if avg_value==None:
                avg_value=0    
            #print(total_avg,sum_value,avg_value)

            if not ('pertable' in request.session):
                obj= UserPreference.objects.filter(user=request.user).first()
                if obj:
                    request.session['pertable']=obj.pertable
                else:# nothing in db
                    request.session['pertable']= 10
            else:
                obj= UserPreference.objects.filter(user=request.user).first()
                if obj:
                    request.session['pertable']=obj.pertable
                else:# nothing in db
                    request.session['pertable']= 10
            pertable=request.session['pertable']
        

            obj_paginator = Paginator(queryset, pertable)
            first_page = obj_paginator.page(1).object_list
            #current_page = obj_paginator.get_page(1)
            page_range = obj_paginator.page_range
            
            page_no = request.POST.get('page_no', None)
            if page_no== None:
                page_no=1 
            num_of_pages= int(obj_paginator.num_pages)
            totalrecords= int(obj_paginator.count)
            current_page = obj_paginator.get_page(page_no)    
            
            
            data={}	
            data["per_table"]=pertable
            data["page_no"]=page_no
            data["num_of_pages"]=num_of_pages
            data["totalrecords"]=totalrecords
                #data["has_previous"]=False
            if current_page.has_previous():
                data["has_previous"]=True  
                data["first"]=1 
                data["previous_page_number"]=current_page.previous_page_number() 
            
            data["current_page"]=current_page.number     
            
            #data["has_next"]=False
            if current_page.has_next():
                data["has_next"]=True  
                data["next_page_number"]=current_page.next_page_number()
            
            data["last"]=current_page.paginator.num_pages 
        

            
            if int(page_no)>int(num_of_pages):			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]


            for i in obj_paginator.page(page_no).object_list:			
                
                item_object = model_to_dict(i)
                
                if i.order:
                    if isinstance(i.order.customer.details, User):
                            item_object['customer_details']=i.order.customer.details.username
                    else:
                        item_object['customer_details']= i.order.customer.details
                else:
                    item_object['customer_details'] =None 

                item_object['date_added']=i.date_added.ctime()

                if i.order:
                    item_object['on']= i.order.id
                    if i.order.currency:
                        item_object['currency_symbol']= i.order.currency.symbol
                    else:
                        item_object['currency_symbol']= '$'
                else:
                    item_object['currency_symbol']= '$'
                    item_object['on']= None

                
                item_object['total']= i.total
                if i.product:
                    item_object['price']= i.product.price
                    item_object['prn']= i.product.id
                    item_object['product']= i.product.name
                else:
                    item_object['price']=None
                    item_object['prn']=None
                    item_object['product']= None
                        
                results.append(item_object)									 
            
                
            data["results"]=results
            data["total_sum"]=float(round(sum_value,2))
            data["average"]=float(round(avg_value,2))
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})
def client_search_and_tags_ajax(request,status, slug, search_type, *args, **kwargs):
    current_time =timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        if search_type == 1:
            if status =="wip":
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=False),Q(product__description__icontains=slug)).order_by('-order__id').order_by('-order__date_ordered')
   
            elif status =="ready": 
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=True),Q(fullfilled=False),Q(product__description__icontains=slug) ).order_by('-order__id').order_by('-order__date_ordered')
   
            elif status =="fullfilled":
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(fullfilled=True), Q(product__description__icontains=slug)).order_by('-order__id').order_by('-order__date_ordered')
   
            else:
                #allll
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(product__description__icontains=slug)).order_by('-order__id').order_by('-order__date_ordered')
            
           
        else:
            if status =="wip":
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=False)).order_by('-order__id').order_by('-order__date_ordered')
   
            elif status =="ready": 
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=True),Q(fullfilled=False)).order_by('-order__id').order_by('-order__date_ordered')
   
            elif status =="fullfilled":
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(fullfilled=True)).order_by('-order__id').order_by('-order__date_ordered')
   
            else:
                #allll
                queryset = OrderItem.objects.filter(Q(product__created_by=request.user)).order_by('-order__id').order_by('-order__date_ordered')
        
        sum_value=0
        avg_value=0     
        #total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
        #sum_value=total_avg['sum']
        #avg_value=total_avg['avg']
        if sum_value==None:
            sum_value=0
        if avg_value==None:
            avg_value=0 

        if not ('pertable' in request.session):
            obj= UserPreference.objects.filter(user=request.user).first()
            if obj:
                request.session['pertable']=obj.pertable
            else:# nothing in db
                request.session['pertable']= 10
        else:
            obj= UserPreference.objects.filter(user=request.user).first()
            if obj:
                request.session['pertable']=obj.pertable
            else:# nothing in db
                request.session['pertable']= 10

        pertable=request.session['pertable']
    

        obj_paginator = Paginator(queryset, pertable)
        first_page = obj_paginator.page(1).object_list
        # = obj_paginator.get_page(1)
        page_range = obj_paginator.page_range
        
        page_no = request.POST.get('page_no', None)
        if page_no== None:
            page_no=1
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
        current_page = obj_paginator.get_page(page_no)    
        
        
        data={}	
        data["per_table"]=pertable
        data["page_no"]=page_no
        data["num_of_pages"]=num_of_pages
        data["totalrecords"]=totalrecords
            #data["has_previous"]=False
        if current_page.has_previous():
            data["has_previous"]=True  
            data["first"]=1 
            data["previous_page_number"]=current_page.previous_page_number() 
        
        data["current_page"]=current_page.number     
        
        #data["has_next"]=False
        if current_page.has_next():
            data["has_next"]=True  
            data["next_page_number"]=current_page.next_page_number()
        
        data["last"]=current_page.paginator.num_pages 
    

            
        if int(page_no)>int(num_of_pages):			
            data["results"]=[]
            return JsonResponse({"data":data})
        results=[]


        for i in obj_paginator.page(page_no).object_list:
            item_object = model_to_dict(i)
            if i.order:
                if isinstance(i.order.customer.details, User):
                        item_object['customer_details']=i.order.customer.details.username
                else:
                    item_object['customer_details']= i.order.customer.details
            else:
                item_object['customer_details'] =None 

            item_object['date_added']=i.date_added.ctime()

            if i.order:
                item_object['on']= i.order.id
                if i.order.currency:
                    item_object['currency_symbol']= i.order.currency.symbol
                else:
                    item_object['currency_symbol']= '$'
            else:
                item_object['currency_symbol']= '$'
                item_object['on']= None

            
            item_object['total']= i.total
            if i.product:
                item_object['price']= i.product.price
                item_object['prn']= i.product.id
                item_object['product']= i.product.name
            else:
                item_object['price']=None
                item_object['prn']=None
                item_object['product']= None

            
            results.append(item_object)									 
        
            
        data["results"]=results
        data["total_sum"]=float(round(sum_value,2))
        data["average"]=float(round(avg_value,2))
        return JsonResponse({"data":data})
    else:
        return JsonResponse({'error': True, 'data': 'errors'})  
    

def display_userorders_ajax(request):
    current_time = timezone.now()#datetime.datetime.now()
    
    userdata= Order.objects.filter(customer__user=request.user)

    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 3
    pertable=request.session['pertable']
    obj_paginator = Paginator(userdata, pertable)
    first_page = obj_paginator.page(1).object_list
    page_range = obj_paginator.page_range
    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None)
        #print('page:', page_no) 
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
        current_page = obj_paginator.get_page(page_no)   
        data={}	
        data["per_table"]=pertable
        data["page_no"]=page_no
        data["num_of_pages"]=num_of_pages
        data["totalrecords"]=totalrecords
        
        #data["has_previous"]=False
        if current_page.has_previous():
            data["has_previous"]=True  
            data["first"]=1 
            data["previous_page_number"]=current_page.previous_page_number() 
        
        data["current_page"]=current_page.number     
        
        #data["has_next"]=False
        if current_page.has_next():
            data["has_next"]=True  
            data["next_page_number"]=current_page.next_page_number()
        
        data["last"]=current_page.paginator.num_pages 
        if int(page_no)>int(num_of_pages):			
            data["results"]=[]
            return JsonResponse({"data":data})

                                                
        results=[] 												 
        for i in obj_paginator.page(page_no).object_list:

            item_object = model_to_dict(i)
            #print (type(i.customer.details))
            if isinstance(i.customer.details, User):
                    item_object['customer_details']=i.customer.details.username
            else:
                item_object['customer_details']= i.customer.details
            item_object['date_ordered']=i.date_ordered.ctime()
            if i.currency:
                item_object['currency_symbol']= i.currency.symbol
            else:
                item_object['currency_symbol']= '$'
            item_object['total_price']= i.total_price
           
            results.append(item_object)
		
        data["results"]=results
        return JsonResponse({"data":data})


def product_search_and_tags_ajax(request, slug, search_type, *args, **kwargs):
    #search my products
    current_time =timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        if search_type == 1:
            queryset = Product.objects.filter(Q(created_by=request.user), Q(description__icontains=slug) )
        else:
            queryset = Product.objects.filter(Q(created_by=request.user))
          
        total_avg= queryset.aggregate(sum=Sum('price'), avg=Avg('price'))
        sum_value=total_avg['sum']
        avg_value=total_avg['avg']
        if sum_value==None:
            sum_value=0
        if avg_value==None:
            avg_value=0 

        if not ('pertable' in request.session):
            obj= UserPreference.objects.filter(user=request.user).first()
            if obj:
                request.session['pertable']=obj.pertable
            else:# nothing in db
                request.session['pertable']= 10
        else:
            obj= UserPreference.objects.filter(user=request.user).first()
            if obj:
                request.session['pertable']=obj.pertable
            else:# nothing in db
                request.session['pertable']= 10

        pertable=request.session['pertable']
    

        obj_paginator = Paginator(queryset, pertable)
        first_page = obj_paginator.page(1).object_list
        # = obj_paginator.get_page(1)
        page_range = obj_paginator.page_range
        
        page_no = request.POST.get('page_no', None)
        if page_no== None:
            page_no=1
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
        current_page = obj_paginator.get_page(page_no)    
        
        
        data={}	
        data["per_table"]=pertable
        data["page_no"]=page_no
        data["num_of_pages"]=num_of_pages
        data["totalrecords"]=totalrecords
            #data["has_previous"]=False
        if current_page.has_previous():
            data["has_previous"]=True  
            data["first"]=1 
            data["previous_page_number"]=current_page.previous_page_number() 
        
        data["current_page"]=current_page.number     
        
        #data["has_next"]=False
        if current_page.has_next():
            data["has_next"]=True  
            data["next_page_number"]=current_page.next_page_number()
        
        data["last"]=current_page.paginator.num_pages 
    

            
        if int(page_no)>int(num_of_pages):			
            data["results"]=[]
            return JsonResponse({"data":data})
        results=[]


        for i in obj_paginator.page(page_no).object_list:			
            cdate= i.date_created.ctime()
            item_object = model_to_dict(i)
            
            categories = ''
          
            for x in item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            item_object['categories']=  categories[:len(categories)-2]
          
            
            if i.image:
                item_object['image']= i.image.url
            else:
                item_object['image']=None
           
            results.append(item_object)									 
            
            									 
        
            
        data["results"]=results
        data["total_sum"]=float(round(sum_value,2))
        data["average"]=float(round(avg_value,2))
        return JsonResponse({"data":data})
    else:
        return JsonResponse({'error': True, 'data': 'errors'})  
  
def get_user_products_load_status_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
           
            queryset = Product.objects.filter(Q(created_by=request.user))
            total_avg= queryset.aggregate(sum=Sum('price'), avg=Avg('price'))
            sum_value=total_avg['sum']
            avg_value=total_avg['avg']
            if sum_value==None:
                sum_value=0
            if avg_value==None:
                avg_value=0    
            #print(total_avg,sum_value,avg_value)

            if not ('pertable' in request.session):
                obj= UserPreference.objects.filter(user=request.user).first()
                if obj:
                    request.session['pertable']=obj.pertable
                else:# nothing in db
                    request.session['pertable']= 10
            else:
                obj= UserPreference.objects.filter(user=request.user).first()
                if obj:
                    request.session['pertable']=obj.pertable
                else:# nothing in db
                    request.session['pertable']= 10
            pertable=request.session['pertable']
        

            obj_paginator = Paginator(queryset, pertable)
            first_page = obj_paginator.page(1).object_list
            #current_page = obj_paginator.get_page(1)
            page_range = obj_paginator.page_range
            
            page_no = request.POST.get('page_no', None)
            if page_no== None:
                page_no=1 
            num_of_pages= int(obj_paginator.num_pages)
            totalrecords= int(obj_paginator.count)
            current_page = obj_paginator.get_page(page_no)    
            
            
            data={}	
            data["per_table"]=pertable
            data["page_no"]=page_no
            data["num_of_pages"]=num_of_pages
            data["totalrecords"]=totalrecords
                #data["has_previous"]=False
            if current_page.has_previous():
                data["has_previous"]=True  
                data["first"]=1 
                data["previous_page_number"]=current_page.previous_page_number() 
            
            data["current_page"]=current_page.number     
            
            #data["has_next"]=False
            if current_page.has_next():
                data["has_next"]=True  
                data["next_page_number"]=current_page.next_page_number()
            
            data["last"]=current_page.paginator.num_pages 
        

            
            if int(page_no)>int(num_of_pages):			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]


            for i in obj_paginator.page(page_no).object_list:			
                cdate= i.date_created.ctime()
                item_object = model_to_dict(i)
              
                categories=""
                for x in item_object['categories']:
                    categories = categories +   str(x.name) + ', '  
                item_object['categories']=  categories[:len(categories)-2]
                if i.image:
                    item_object['image']= i.image.url
                else:
                    item_object['image']=None
               
                    
                
                results.append(item_object)									 
            
                
            data["results"]=results
            data["total_sum"]=float(round(sum_value,2))
            data["average"]=float(round(avg_value,2))
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})
def get_user_orders_load_status_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
           
            queryset = Order.objects.filter(Q(customer__user=request.user))
            # total_avg= queryset.aggregate(sum=Sum('price'), avg=Avg('price'))
            # sum_value=total_avg['sum']
            # avg_value=total_avg['avg']
            sum_value=0
            avg_value=0 
            if sum_value==None:
                sum_value=0
            if avg_value==None:
                avg_value=0    
            #print(total_avg,sum_value,avg_value)

            if not ('pertable' in request.session):
                obj= UserPreference.objects.filter(user=request.user).first()
                if obj:
                    request.session['pertable']=obj.pertable
                else:# nothing in db
                    request.session['pertable']= 10
            else:
                obj= UserPreference.objects.filter(user=request.user).first()
                if obj:
                    request.session['pertable']=obj.pertable
                else:# nothing in db
                    request.session['pertable']= 10
            pertable=request.session['pertable']
        

            obj_paginator = Paginator(queryset, pertable)
            first_page = obj_paginator.page(1).object_list
            #current_page = obj_paginator.get_page(1)
            page_range = obj_paginator.page_range
            
            page_no = request.POST.get('page_no', None)
            if page_no== None:
                page_no=1 
            num_of_pages= int(obj_paginator.num_pages)
            totalrecords= int(obj_paginator.count)
            current_page = obj_paginator.get_page(page_no)    
            
            
            data={}	
            data["per_table"]=pertable
            data["page_no"]=page_no
            data["num_of_pages"]=num_of_pages
            data["totalrecords"]=totalrecords
                #data["has_previous"]=False
            if current_page.has_previous():
                data["has_previous"]=True  
                data["first"]=1 
                data["previous_page_number"]=current_page.previous_page_number() 
            
            data["current_page"]=current_page.number     
            
            #data["has_next"]=False
            if current_page.has_next():
                data["has_next"]=True  
                data["next_page_number"]=current_page.next_page_number()
            
            data["last"]=current_page.paginator.num_pages 
        

            
            if int(page_no)>int(num_of_pages):			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]


            for i in obj_paginator.page(page_no).object_list:			
                #cdate= i.date_created.ctime()
                item_object = model_to_dict(i)
                #print (type(i.customer.details))
                if isinstance(i.customer.details, User):
                     item_object['customer_details']=i.customer.details.username
                else:
                    item_object['customer_details']= i.customer.details
                item_object['date_ordered']=i.date_ordered.ctime()
                if i.currency:
                    item_object['currency_symbol']= i.currency.symbol
                else:
                    item_object['currency_symbol']= '$'
                item_object['total_price']= i.total_price
              
              
              
                
                results.append(item_object)									 
            
            #print(results)    
            data["results"]=results
            data["total_sum"]=float(round(sum_value,2))
            data["average"]=float(round(avg_value,2))
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})

login_required(login_url="account_login")
def make_invoice_from_order(request, pk):
    current_order = get_object_or_404(Order,pk=pk)
    invoice = Invoice.objects.filter(parentorder=current_order).first()
    user_company= CompanyUser.objects.filter(user=request.user)
    item_sbu =[]
    if user_company :
        item_sbu = list(user_company.values_list('company', flat=True))
        first_company = Company.objects.filter(pk__in=item_sbu).first()
    else:
        first_company = Company.objects.first()
    
    if not invoice:
        #-----get latest invoice n# if exist or create 1-------------
        try:
            latest_i_num = Invoice.objects.latest('id').number
            auto_invoice_num= int(latest_i_num) + 1
        except Invoice.DoesNotExist:
            auto_invoice_num =  1
        #-----------------------------------------
        #------------save the invoice------------------
        invoice = Invoice(company=first_company, parentorder=current_order, 
                        customer=current_order.customer,number=auto_invoice_num,
                        date=datetime.date.today(), status='Unpaid')
        invoice.save()
        
        order_items = OrderItem.objects.filter(order=current_order)
        #--add invoice items
        for o_item in order_items:
            invoice_items = InvoiceItem(product=o_item.product, qty=o_item.quantity, 
                            invoice=invoice, cost=o_item.product.price)
            invoice_items.save() 

    products = Product.objects.all().order_by('name')
    currencys = Currency.objects.order_by('name') 
    companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
    context = {
        'title' : 'Invoice ' + str(invoice.id),
        'invoice' : invoice,
        'product_list' : products,
        'currency_list' : currencys,
        'company_list' : companys,
    }
    return render(request, 'invoices/invoice.html', context)


def save_all(request,form,template_name):
    data = dict()
    #print(form.errors)
    #print('am i here.........?',request.method,"Form valid?", form.is_valid() )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            #print(form.instance.id)
            data['form_is_valid'] = True
            
            # retrieve product
            pk = form.instance.id
            product = get_object_or_404(Product,pk=pk)
            product_item_object = model_to_dict(product)
            product_item_object['image']=str(product_item_object['image'])
            categories=""
            for x in product_item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            product_item_object['categories']=  categories[:len(categories)-2]
          
            companies=""
            for x in product_item_object['company']:
                companies  = companies + str(x.name)  
            product_item_object['company']=  companies
            data['product'] = product_item_object
        else:
            data['form_is_valid'] = False
    context = {
    'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    #print(data)
    return JsonResponse(data)

login_required(login_url="account_login")
def product_update(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=product)
    else:
        form = ProductUpdateForm(instance=product)
    return save_all(request,form,'customers/product_edit_modal.html')



@login_required(login_url="account_login")
def unlockProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST' and request.is_ajax():
        try:
            product.locked=False
            product.save()
            product_item_object = model_to_dict(Product.objects.get(pk=pk))
            
            product_item_object['image']=str(product_item_object['image'])
            categories=""
            
            for x in product_item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            product_item_object['categories']=  categories[:len(categories)-2]
          
            companies=""
            for x in product_item_object['company']:
                companies  = companies + str(x.name)  
            product_item_object['company']=  companies
            
            return JsonResponse({'error': False, 'data': product_item_object})
            
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'message': 'Record does not exist.'})
    return JsonResponse({'status': 'Fail', 'message': 'Error, must be an Ajax call.'})
@login_required(login_url="account_login")
def lockProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST' and request.is_ajax():
        try:
            product.locked=True
            product.save()
            product_item_object = model_to_dict(Product.objects.get(pk=pk))
           
            product_item_object['image']= str(product_item_object['image'])
            categories=""
            
            for x in product_item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            product_item_object['categories']=  categories[:len(categories)-2]
          
            
            companies=""
            for x in product_item_object['company']:
                companies  = companies + str(x.name)  
            product_item_object['company']=  companies
            
            return JsonResponse({'error': False, 'data': product_item_object})
           
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'message': 'Record does not exist.'})
    return JsonResponse({'status': 'Fail', 'message': 'Error, must be an Ajax call.'})

@login_required(login_url="account_login")
def edit_product_details(request):
    if request.method == 'POST':
        # Fetching data from the add new home address form
        employee_id = request.POST['employee_id']
        depart = request.POST['depart']
        position = request.POST['position']
        team = request.POST['team']

        # Get the employee instance
        employee = Employee.objects.get(pk=employee_id)
        # Get the department instance
        department = Department.objects.get(pk=depart)
        team = Team.objects.get(pk=team)
        position = Position.objects.get(pk=position)
        # get instance of organisation Detail
        organisation_detail = OrganisationDetail.objects.get(employee=employee)
        organisation_detail.department = department
        organisation_detail.position = position
        organisation_detail.team = team
        # Saving the BankDetail instance
        organisation_detail.save()
        context = {
            "employees_page": "active",
            "success_msg": "You have successfully updated %s Organisation Details " % (employee.first_name),
            "employee": employee
        }

        return render(request, 'employees/success.html', context)

    else:
        context = {
            "employees_page": "active",
            "failed_msg": "Failed! You performed a GET request"
        }

        return render(request, "employees/failed.html", context)

def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['bakasa.andrew@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('products')

@login_required(login_url="account_login")
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk, created_by =request.user)
    if request.method == "POST":
        product.delete()
        return redirect("products")

    context = {'item': product}
    return render(request, 'customers/delete_product.html', context)

@login_required(login_url="account_login")
def delete_product_ajax(request, id, page_no, *args, **kwargs):
   
    if request.method == 'POST':
        #print(request.POST)
        if request.is_ajax():
            
            model_ = get_object_or_404(Product, pk=id)
          
            item_object = model_to_dict(model_)
           
            
          
            data= {}
            #data['total_pages']=total_pages
            data['deleted_page']=page_no
            
           

            #print('>>>>>>>>', item_object)
            
            categories=""
            for x in item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            item_object['categories']=  categories[:len(categories)-2]
            if model_.image:
                item_object['image']= model_.image.url
            else:
                item_object['image']=None
            data['model']=item_object
            model_.delete()
            
            return JsonResponse({'error': False, 'data': data})
            
        else:
            return JsonResponse({'error': True, 'data': "errors encontered"})
    else:
        error = {
            'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json") 
class ProductCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Product
    template_name = 'customers/product_edit.html'
    success_url = reverse_lazy('user_products')

    def get_form_class(self):
        return ProductForm

   
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        #self.object = self.get_object() # assign the object to the view
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        # files = request.FILES.getlist('file_field')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #print(request.FILES)
        
        form = ProductForm(request.POST,request.FILES) # class based view.
        if form.is_valid():
            # for f in files:
            #     ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

#----defunct-----11 march2021
def update_product(request, pk):
    error_message=None
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES)
        #print(form)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect(reverse('products', ))
    else:
        try :
            product = get_object_or_404(Product,pk=pk)
            form = ProductUpdateForm(instance=product)
        except Product.DoesNotExist:
            error_message ="Product not found"
            
    context ={'form': form, 'error_message': error_message}
    return render(request, 'customers/product_edit.html', context)

class AjaxableResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        print(context)
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response

class  ProductUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    form_class= ProductForm
    model = Product
    template_name = 'customers/product_edit_modal.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # assign the object to the view
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        
        pk = kwargs.get('pk', None)
        product = get_object_or_404(Product, pk=pk)
        #print(request.POST)
        #print(request.FILES)
       
        form = ProductForm(request.POST or None, request.FILES or None, instance=product) # class based view.
        #print(form)
        data =  dict()
        if form.is_valid():
            product= form.save()

            product_item_object =model_to_dict(product)
            product_item_object['image']=str(product_item_object['image'])
            categories=""
           
            for x in product_item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            product_item_object['categories']=  categories[:len(categories)-2]
          
            
            companies=""
            for x in product_item_object['company']:
                companies  = companies + str(x.name)  
            product_item_object['company']=  companies
            

            data['product'] = product_item_object
        else:
            data['error'] =  "form not valid!"
        return JsonResponse(data)
   

      
class ProductUpdateView(LoginRequiredMixin, AjaxableResponseMixin, generic.edit.UpdateView):
    #template_name = 'customers/product_edit.html'
    template_name = 'customers/product_edit_modal.html'
    #template_name = 'customers/products.html'
    model = Product
    success_url = reverse_lazy('products')

    form_class= ProductForm

    # def get_initial(self):
    #     initial = super().get_initial()
    #     #print(initial)
    #     return initial

    # def get_form_class(self):
    #     return ProductForm


    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # assign the object to the view
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        
        pk = kwargs.get('pk', None)
        product = get_object_or_404(Product, pk=pk)

        form = ProductForm(request.POST or None, request.FILES or None,instance=product) # class based view.
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return generic.edit.ProcessFormView.get(self, request, *args, **kwargs)
    
   

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):
		order_id= kwargs.get('order_id', None)
		order = get_object_or_404(Order, pk=order_id)	
	
		context = {
			'title' : "Order " + str(order_id),
			'order' : order,
		}
		
		pdf = render_to_pdf('customers/printhtml2pdf.html', context)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		order_id= kwargs.get('order_id', None)
		order = get_object_or_404(Order, pk=order_id)	

		context = {
			'title' : "Order " + str(order_id),
			'order' : order,
		}	
		
		pdf = render_to_pdf('customers/printhtml2pdf.html', context)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Order_%s.pdf" %(order.id)
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response



@login_required(login_url="account_login")
#divert customer and allow all other
@registered_user_only_with_client_routing()
def home(request):
    orders = Order.objects.all()
    # use aggegation and check the most important customer in last year
    # aggerate on sales/ income by each custome of ours....
    # use analytic to rank customers
    customers = Customer.objects.filter(coporateclient=True).order_by('-pk')[:5]

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(complete=True).count()
    pending = orders.filter(complete=False).count()
    
    # latest 5 orders
    orders=Order.objects.filter(complete=True).order_by('-pk')[:5]
    context = { 
    'orders': orders, 
    'customers': customers,
    'total_orders': total_orders,
    'delivered': delivered,
    'pending': pending,
    'cencelled': 0,
    }
    #print(context)

    return render(request, 'customers/dashboard.html', context)

def userPage(request):
    context = {}
    return render(request, 'customers/user.html', context)

@login_required(login_url="account_login")
def products(request):
    products = Product.objects.filter(created_by=request.user)
    productcategories = ProductCategory.objects.all()
    context ={'products': products, 'categories':productcategories}
    return render(request, 'customers/user_products.html', context)



class ProductsIndex(LoginRequiredMixin,  generic.ListView):
    template_name = 'customers/user_products.html'
    context_object_name = 'products'
    model = Product
    page_pagenated= "0"
    dynamic_search_mode=''
   
    
    try:
        self.dynamic_search_mode = self.request.COOKIES['dynamic_search_mode']
        if len(self.dynamic_search_mode)>0:
            #2.(a) remove pagenation
            self.page_pagenated= "0" # for
            paginate_by = None
        else:
            #1.(b)
            self.page_pagenated= "1" # no search :paginate
            paginate_by = 7
    except:
        paginate_by = 7  # no cookie set yet
        page_pagenated= "1" # no search :paginate
    
    def get_queryset(self):
        # print(self.request.GET)
        # search_product_string = self.request.COOKIES['search_product_string']
        products = Product.objects.filter(created_by=self.request.user)
        return products
   
    def get_context_data(self, **kwargs):
        try:
            #1.(a)... first time there is no cookie or string is zero            
            self.dynamic_search_mode = self.request.COOKIES['dynamic_search_mode']
            if len(self.dynamic_search_mode)>0:
                self.page_pagenated= "0" # for
                self.paginate_by = None
            else:
                #1.(b)
                self.page_pagenated= "1" # no search :paginate
                self.paginate_by = 7
        except:
            self.paginate_by = 7  # no cookie set yet
            self.page_pagenated= "1" # no search :paginate
        
        
        context = super().get_context_data(**kwargs)

        context['page_pagenated'] = str(self.page_pagenated)
         #get user group credentials
        user_group_set =get_current_user_groups(self.request.user)
        context['lock_key'] = True if 'admin' in user_group_set else False
        #any of two role
        context['edit_key'] = True if any(role in user_group_set for role in ('editor', 'admin')) else False
        
        context['form'] = ProductForm
        return context
   

@login_required(login_url="account_login")
def orders(request):

    BUSINESS_STATUS_CHOICE = ["all"]#["unread","open","closed","all"] 
   
    queryset = Order.objects.filter(Q(customer__user=request.user))
    
    sum_value=0
    avg_value=0
    #print('My orders...........')
    #print(queryset)
    # total_avg= queryset.aggregate(sum=Sum('total_price'), avg=Avg('total_price'))
    # sum_value=total_avg['sum']
    # avg_value=total_avg['avg']
    if sum_value==None:
        sum_value=0
    if avg_value==None:
        avg_value=0  
    form = ProductForm(initial={'created_by': request.user})
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    else:
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    pertable=request.session['pertable']

    obj_paginator = Paginator(queryset, pertable)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
         'orders':first_page,
        'current_page':current_page,
        'page_range':page_range,
        "user": request.user,
        "models": queryset,
        "total": queryset.count(),
        "user": request.user,
        'form': form,
         'status': type,
        "BUSINESS_STATUS_CHOICE": BUSINESS_STATUS_CHOICE,
        "total_sum": float(round(sum_value,2)),
        "average": round(avg_value,2),
        'lock_key':True,
        'edit_key':True
    }
   
    return render(request, 'customers/orders_list.html', context)

@login_required(login_url="account_login")
def get_user_clients(request, type):

    BUSINESS_STATUS_CHOICE = ["wip","ready","fullfilled", 'all'] 
   
    queryset = OrderItem.objects.filter(Q(product__created_by=request.user)).order_by('-order__id').order_by('-order__date_ordered')
    
    if type =="wip":
        queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=False)).order_by('-order__id').order_by('-order__date_ordered')

    elif type =="ready": 
        queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(order__complete=True),Q(fullfilled=False)).order_by('-order__id').order_by('-order__date_ordered')

    elif type =="fullfilled":
        queryset = OrderItem.objects.filter(Q(product__created_by=request.user),Q(fullfilled=True)).order_by('-order__id').order_by('-order__date_ordered')

    else:
        #all
        queryset = OrderItem.objects.filter(Q(product__created_by=request.user)).order_by('-order__id').order_by('-order__date_ordered')
    
    
    sum_value=0
    avg_value=0
    # print('My clients...........')
    # print(queryset)
    # total_avg= queryset.aggregate(sum=Sum('total_price'), avg=Avg('total_price'))
    # sum_value=total_avg['sum']
    # avg_value=total_avg['avg']
    if sum_value==None:
        sum_value=0
    if avg_value==None:
        avg_value=0  
    form = ProductForm(initial={'created_by': request.user})
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    else:
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    pertable=request.session['pertable']

    obj_paginator = Paginator(queryset, pertable)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
         'orders':first_page,
        'current_page':current_page,
        'page_range':page_range,
        "user": request.user,
        "models": queryset,
        "total": queryset.count(),
        "user": request.user,
        'form': form,
        'status': type,
        "BUSINESS_STATUS_CHOICE": BUSINESS_STATUS_CHOICE,
        "total_sum": float(round(sum_value,2)),
        "average": round(avg_value,2),
        'lock_key':True,
        'edit_key':True
    }
   
    return render(request, 'customers/clients_list.html', context)


class OrdersIndex(LoginRequiredMixin, generic.ListView):
    template_name = 'customers/orders_list.html'
    context_object_name = 'orders'
    model = Order
    paginate_by = 5
    # context ={}

    def dispatch(self, request, *args, **kwargs):
        self.complete_status = kwargs.pop('complete_status')
        return super(OrdersIndex, self).dispatch(request, *args, **kwargs)

  
    def get_queryset(self):
        #limit my order
        print('User object', self.request.user)
        customer = get_object_or_404(Customer, user=self.request.user)
        orders = Order.objects.filter(customer =customer)

        #----inject to filter completed order only
        if len(self.request.GET)==0 and self.complete_status =="True": 
            print('found...')
            default_dict= {'complete': 'true'}
            self.myFilter = OrderFilter(default_dict, queryset=orders)
        else:
            self.myFilter = OrderFilter(self.request.GET, queryset=orders)
        
                
        orders = self.myFilter.qs
        return orders

    def get_context_data(self, **kwargs):
        #print(self.myFilter)
        context = super().get_context_data(**kwargs)
        context['myFilter']= self.myFilter
        # context['orders'] = self.orders 
        return context
    


@login_required(login_url="account_login")
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    total_per_page = 10
     # add---
    paginator = Paginator(orders, total_per_page) # Show 25 contacts per page
    page = request.GET.get('page')
    
    try:
        orders = paginator.get_page(page)
    except PageNotAnInteger :
        orders = paginator.get_page(1)
    except EmpytPage:
        orders = paginator.get_page(paginator.num_pages)
     
    is_paginated = False
    #pagenate only if greter than num of list per page
    if  int(paginator.num_pages) > 1 :
       is_paginated = True

    # print("Paginated?:=" + str(is_paginated) + " max per Page:=" + str(total_per_page) +  " Total Pages:= " + str(paginator.num_pages))
    
    context = {
    'customer': customer, 
    'orders': orders, 
    'order_count': order_count,
    'myFilter': myFilter,
    'page_obj': orders,
    'is_paginated' : is_paginated,
    }


    return render(request, 'customers/customer.html', context)

@login_required(login_url="account_login")
def customers(request):
    customers = Customer.objects.all()


    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs

    context = {
    'customers': customers,
    'myFilter': myFilter
    }
   
    return render(request, 'customers/customers_list.html', context)

@login_required(login_url="account_login")
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'complete'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            # return redirect("/")
            return redirect("customers_home")

    context = {'formset': formset}
    return render(request, 'customers/order_form_set.html', context)




@login_required(login_url="account_login")
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("orders_list")

    context = {'item': order}
    return render(request, 'customers/delete_order.html', context)

@login_required(login_url="account_login")
def deleteOrder_ajax(request, pk):
    Float_thousand ="{:,.2f}"
    if request.method == 'POST' and request.is_ajax():
        try:
            
            item = get_object_or_404(Order, pk=pk)
           
            item_object = {}
            
            item_object["item"]= 'Item has been deleted'
            #item_object["order_total"] =  item
            item.delete()

            return JsonResponse({'status': 'Success', 'message': 'Record has been deleted.', 'data': item_object})
            
        except InvoiceItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'message': 'Record does not exist.'})
    return JsonResponse({'status': 'Fail', 'message': 'Error, must be an Ajax call.'})

@login_required(login_url="account_login")
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("customers_home")

    context = {'item': customer}
    return render(request, 'customers/delete_customer.html', context)


class CustomerCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Customer
    template_name = 'customers/customer_edit.html'
    success_url = reverse_lazy('customers_list')

    def get_form_class(self):
        return CustomerForm

    def get_context_data(self, **kwargs):
        context = super(CustomerCreate, self).get_context_data(**kwargs)
        context['menu'] = 'customers'
        context['submenu'] = "customer" #self.type
        return context


# Display a specific invoice
@login_required(login_url="account_login")
def order(request, order_id):
    #throw erro if user order doesnt belong to user
    order = get_object_or_404(Order, pk=order_id, customer__user=request.user)
    
    #----------------------------------------------
    invoice = Invoice.objects.filter(parentorder=order)
    
    if invoice:
        invoiced = True
    else:
        invoiced = False
    #----------------------------------------------

    products = Product.objects.filter(created_by=request.user)
    currencys = Currency.objects.order_by('name') 
    context = {
        'title' : 'Order ' + str(order_id),
        'order' : order,
        'product_list' : products,
        'currency_list' : currencys,
        'invoiced' : invoiced,
    }
    return render(request, 'customers/order.html', context)  
# Display a specific invoice
@login_required(login_url="account_login")
def order_registered(request, order_id):
    #print("uncompleted order is still avialable")
    order = get_object_or_404(Order, pk=order_id)
    products = Product.objects.filter(created_by=request.user)
    currencys = Currency.objects.order_by('name') 
    context = {
        'title' : 'Order ' + str(order_id),
        'order' : order,
        'product_list' : products,
        'currency_list' : currencys,
        'error_message' : 'Cannot create new order until this is closed.',
    }
    return render(request, 'customers/order.html', context)  


@login_required(login_url="account_login")
def products_search(request, search_string):
    if request.method == 'POST' and request.is_ajax():
        try:
            search_string = request.POST['search_string']
            qs = Product.objects.filter(name__icontains=search_string)
            productitems = []
            for product in qs:
                productcategoryitems=[]
                for cat in product.categories.all():
                    productcategory= {               
                        'name': cat.name,
                    }
                    productcategoryitems.append(productcategory)
                productitem = {
                        'categories': productcategoryitems,
                        'name': product.name,
                        'description': product.description,
                        'image': product.image,
                        'price': product.price,
                }
                productitems.append(productitem)

            return JsonResponse({'status': 'Success', 'message': 'Querset found.', 'data': productitems})
            
        except Product.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'message': 'Records does not exist.'})
    return JsonResponse({'status': 'Fail', 'message': 'Error, must be an Ajax call.'})

@login_required(login_url="account_login")
def delete_item(request, orderitem_id, order_id):
    Float_thousand ="{:,.2f}"
    if request.method == 'POST' and request.is_ajax():
        try:
            
            item = get_object_or_404(OrderItem, pk=orderitem_id)
            item.delete()
            order = get_object_or_404(Order, pk=order_id)
            order_item_object = {}
            
            order_item_object["currency_symbol"]= order.currency.symbol if order.currency else ''
            order_item_object["order_total"] =  Float_thousand.format(order.total_price)
            #print (order_item_object) 

            return JsonResponse({'status': 'Success', 'message': 'Record has been deleted.', 'data': order_item_object})
            
        except InvoiceItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'message': 'Record does not exist.'})
    return JsonResponse({'status': 'Fail', 'message': 'Error, must be an Ajax call.'})

@login_required(login_url="account_login")
def add_item(request, order_id):
    Float_thousand ="{:,.2f}"
    order = get_object_or_404(Order, pk=order_id)
    #print("adding item")
    if request.method == 'POST':
        if request.is_ajax():
            product_id = request.POST['product_id']
            # cost = request.POST['cost']
            quantity = request.POST['quantity']
                
            if product_id is not None :
                product = get_object_or_404(Product, pk=product_id)
                i = order.orderitem_set.create(product=product, quantity=quantity)
                i.save()
                latest = OrderItem.objects.latest('id').id
                order_item_object = model_to_dict(OrderItem.objects.get(pk=latest))
                
                # print(order_item_object)
                order_item_object["order_id"]= order.id
                order_item_object["currency_symbol"]= order.currency.symbol if order.currency else ''
                order_item_object["product_name"]= product.name
                order_item_object["product_description"]= product.description
                order_item_object["price"]= product.price
                order_item_object["total"]= product.price * decimal.Decimal(order_item_object["quantity"])

                order_item_object["order_total"] =  Float_thousand.format(order.total_price) # prev_total + order_item_object["total"]

                # print(order_item_object)
                return JsonResponse({'error': False, 'data': order_item_object})
            else:
                # print(createbookform.errors)
                return JsonResponse({'error': True, 'data': "errors encontered"})
        else:
            error = {
                'message': 'Error, must be an Ajax call.'
            }
            return JsonResponse(error, content_type="application/json")
    else:
        return HttpResponseRedirect(reverse('order', args=(order.id,)))


@login_required(login_url="account_login")
def getproduct(request):
    #print("adding item")
    if request.method == 'POST':
        if request.is_ajax():
            product_id = request.POST['product_id']
            if product_id is not None :
                product_item_object = model_to_dict(Product.objects.get(pk=product_id))
                print(product_item_object)
                product_item_object['image']=''
                product_item_object['categories']= [{'name': x.name}  for x in product_item_object['categories']]
                product_item_object['company']= [{'name': x.name}  for x in product_item_object['company']]
                productcategoryitems=[]
                
                """ 
                product_item_object.pop('categories', None) 

                   or
                if 'categories' in my_dict:
                del product_item_object['categories']
                
                """
                # for cat in product_item_object['categories']:
                #     productcategory= {               
                #         'name': cat.name,
                #     }
                #     productcategoryitems.append(productcategory)

               
                print(product_item_object)
                # print(productcategoryitems)
                
                # productitem = {
                #         'categories': productcategoryitems,
                #         'name': product.name,
                #         'description': product.description,
                #         'image': product.image,
                #         'price': product.price,
                # }
                return JsonResponse({'error': False, 'data': product_item_object, 'cat': product_item_object})
            else:
                # print(createbookform.errors)
                return JsonResponse({'error': True, 'data': "errors encontered"})
        else:
            error = {
                'message': 'Error, must be an Ajax call.'
            }
            return JsonResponse(error, content_type="application/json")
    else:
        error = {
                'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json")


# Print invoice
@login_required(login_url="account_login")
def print_order(request, order_id):
    #view own orders
    order = get_object_or_404(Order, pk=order_id,customer__user=request.user)	
	
    context = {
		'title' : "Order " + str(order_id),
	    'order' : order,
	}
    return render(request, 'customers/print_order.html', context)


# Upload attachment for order
@login_required(login_url="account_login")
@allowed_users(allowed_roles=['admin', 'ceo', 'manager', 'editor','datacapture'])
def upload_order_attachment(request, order_id):
    myfile = request.FILES['file']
    order = get_object_or_404(Order, pk=order_id)
    # --------------------this was double loading my files---------15 Jan 2021---
    # fs = FileSystemStorage()
	# # myfile.name
	
    # fs.save(myfile.name, myfile)
    #---------------------Corrected erro of double load-----------------------------
    e = order.orderattachment_set.create(file=myfile, displayname=myfile.name)
    e.save()
    return HttpResponseRedirect(reverse('order', args=(order.id,)))


    	
    	

# Delete attachment from order
@login_required(login_url="account_login")
@allowed_users(allowed_roles=['admin', 'ceo', 'manager', 'editor','datacapture'])
def delete_order_attachment(request, order_id, orderattachment_id):
	order = get_object_or_404(Order, pk=order_id)
	orderattachment = get_object_or_404(OrderAttachment, pk=orderattachment_id)
	try:
        # Giving error to connect use signal in invoice signals Total of 3
		orderattachment.delete()
		# fs = FileSystemStorage()
		# fs.delete(orderattachment)
	except:
		context = {
			'error_message' : "Unable to delete attachment!",
			'order_id' : order_id
		}
		return render(request, 'customers/order.html', context)
	else:
		return HttpResponseRedirect(reverse('order', args=(order.id,)))

# Update invoice
@login_required(login_url="account_login")
def update_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    try:
        order.date_ordered = datetime.datetime.strptime(request.POST['date_ordered'], "%m/%d/%Y")
        order.complete = request.POST['complete']
        order.save()
    except (KeyError, Order.DoesNotExist):
        return render(request, 'customers/order.html', {
            'order': order,
            'error_message': 'Not able to update order!',
        })
    else:
        # currencys = Currency.objects.order_by('name')
        products = Product.objects.all()	
        context = {
            'confirm_update' : True,
            'title' : 'Order ' + str(order_id),
            'order' : order,
            'product_list' : products,
            }
        #return render(request, 'customers/order.html', context)
        return HttpResponseRedirect(reverse('order', args=(order.id,)))

# Create new invoice
@login_required(login_url="account_login")
def new_order(request):
    	
	user_company= CompanyUser.objects.filter(user=request.user)
	item_sbu =[]
	if user_company :
		#manytomany link by pk
		item_sbu = list(user_company.values_list('company', flat=True))
	
	
	# If no customer_id is defined, create a new invoice
	if request.method=='POST':
		customer_id = request.POST['customer_id']
		company_id = request.POST['company_id']
		currency_id = request.POST['currency_id']
		transcation_id = request.POST['transcation_id']

		if customer_id=='None':
			customers = Customer.objects.order_by('name')
			currencys = Currency.objects.order_by('name')
			companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
			context = {
				'title' : 'New Order',
				'customer_list' : customers,
				'company_list' : companys,
				'currency_list' : currencys,
				'error_message' : 'Please select a customer and company.',
				}
			return render(request, 'customers/new_order.html', context)

		elif company_id=='None':
			customers = Customer.objects.order_by('name')
			currencys = Currency.objects.order_by('name')
			companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
			context = {
				'title' : 'New Order',
				'customer_list' : customers,
				'company_list' : companys,
				'currency_list' : currencys,
				'error_message' : 'Please select a company and customer.',
				}
			return render(request, 'customers/new_order.html', context)

		elif currency_id=='None':
			customers = Customer.objects.order_by('name')
			currencys = Currency.objects.order_by('name')
			companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
			context = {
				'title' : 'New Order',
				'customer_list' : customers,
				'company_list' : companys,
				'currency_list' : currencys,
				'error_message' : 'Please select a company and customer.',
				}
			return render(request, 'customers/new_order.html', context)	
		else:
			customer = get_object_or_404(Customer, pk=customer_id)
			company = get_object_or_404(Company, pk=company_id)
			currency = get_object_or_404(Currency, pk=currency_id)
			transaction_id = int(
					request.POST.get("transaction_id")
					if request.POST.get("transaction_id", "") != ""
					else 0
				)
                
			i = Order(customer=customer, transaction_id=transaction_id, currency=currency, 
			     company=company, date_ordered=datetime.date.today(), complete='True')# differenriate with the one enter by user
                 #no two uncompleted order required
			i.save()
			return HttpResponseRedirect(reverse('order', args=(i.id,)))

	else:
		# Customer list needed to populate select field
		customers = Customer.objects.order_by('name')
		currencys = Currency.objects.order_by('name')
		companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
		context = {
			'title' : 'New Order',
			'customer_list' : customers,
			'company_list' : companys,
			'currency_list' : currencys,
		}
		return render(request, 'customers/new_order.html', context)

def new_order_customer(request, customer_pk):

    
    user_company= CompanyUser.objects.filter(user=request.user)
    item_sbu =[]
    if user_company :
        #manytomany link by pk
        item_sbu = list(user_company.values_list('company', flat=True))


    # If no customer_id is defined, create a new invoice
    if request.method=='POST':
        customer_id = request.POST['customer_id']
        company_id = request.POST['company_id']
        currency_id = request.POST['currency_id']
        transcation_id = request.POST['transcation_id']

        if customer_id=='None':
            customers = Customer.objects.order_by('name')
            currencys = Currency.objects.order_by('name')
            companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
            context = {
                'title' : 'New Order',
                'customer_list' : customers,
                'company_list' : companys,
                'currency_list' : currencys,
                'error_message' : 'Please select a customer and company.',
                }
            return render(request, 'customers/new_order.html', context)

        elif company_id=='None':
            customers = Customer.objects.order_by('name')
            currencys = Currency.objects.order_by('name')
            companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
            context = {
                'title' : 'New Order',
                'customer_list' : customers,
                'company_list' : companys,
                'currency_list' : currencys,
                'error_message' : 'Please select a company and customer.',
                }
            return render(request, 'customers/new_order.html', context)

        elif currency_id=='None':
            customers = Customer.objects.order_by('name')
            currencys = Currency.objects.order_by('name')
            companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
            context = {
                'title' : 'New Order',
                'customer_list' : customers,
                'company_list' : companys,
                'currency_list' : currencys,
                'error_message' : 'Please select a company and customer.',
                }
            return render(request, 'customers/new_order.html', context)	
        else:
            customer = get_object_or_404(Customer, pk=customer_id)
            #dont create new order if there is one which is already running...
            order = Order.objects.filter(customer=customer, complete=False).first()
            if order :
                return HttpResponseRedirect(reverse('order', args=(order.id,))) 

            company = get_object_or_404(Company, pk=company_id)
            currency = get_object_or_404(Currency, pk=currency_id)
            transaction_id = int(
                    request.POST.get("transaction_id")
                    if request.POST.get("transaction_id", "") != ""
                    else 0
                )
                
            i = Order(customer=customer, transaction_id=transaction_id, currency=currency, 
                    company=company, date_ordered=datetime.date.today(), complete='True')# differenriate with the one enter by user
                    #no two uncompleted order required
            i.save()
            return HttpResponseRedirect(reverse('order', args=(i.id,)))

    else:
        	
   
        # Customer list needed to populate select field
        customer_instance = get_object_or_404(Customer, pk=customer_pk)
        #dont create new order if there is one which is already running...
        order = Order.objects.filter(customer=customer_instance, complete=False).first()
        if order :
            return HttpResponseRedirect(reverse('order',  args=(order.id,))) 

        customers = Customer.objects.order_by('name')
        currencys = Currency.objects.order_by('name')
        companys = Company.objects.filter(pk__in=item_sbu).order_by('name') 
        context = {
            'title' : 'New Order',
            'customer_list' : customers,
            'company_list' : companys,
            'currency_list' : currencys,
            "customer_instance" : customer_instance,
        }
        return render(request, 'customers/new_order.html', context)



# Accounting report
@login_required(login_url="account_login")
def accounting(request):
	if request.method == 'POST':
		start = datetime.datetime.strptime(request.POST['start'], "%m/%d/%Y")
		end = datetime.datetime.strptime(request.POST['end'], "%m/%d/%Y")
		
		if start > end:
			context = {
				'error_message' : "Start date must be before end date!",
			}
			return render(request, 'customers/accounting.html', context)
		else:
			user_company= CompanyUser.objects.filter(user= request.user)
			item_sbu =[]
			if user_company :
				item_sbu = list(user_company.values_list('company', flat=True))

			

			completedorders = Order.objects.filter(date_ordered__gt=start).filter(date_ordered__lt=end).filter(complete = True).filter(company__in=item_sbu)
			allorders = Order.objects.filter(date_ordered__gt=start).filter(date_ordered__lt=end).filter(company__in=item_sbu)
			# expenses = Expense.objects.filter(date__gt=start).filter(date__lt=end).filter(company__in=item_sbu)
			
			# Sum of all paid invoices
			ordertotal = 0
			currencyTotals = {}
		

			for i in completedorders:
				valuetotal = i.total_price
				rate = i.currency.current_rate if i.currency else 1 #check syntax 16 Jan 2021
				
				ordertotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
				
				symbol = i.currency.symbol if i.currency else "USD"
				if symbol in currencyTotals:
					currencyTotals[symbol] += i.total_price
				else:
					currencyTotals[symbol] = i.total_price

		
			# Add invoice expenses within date range, regardless of invoice status
			
		
			context = {
				'start' : start,
				'end' : end,
				'orders' : completedorders,
				'ordertotal' : ordertotal,
				'currencyTotals' : currencyTotals,
			}
			return render(request, 'customers/accounting.html', context)
	else:# default current month
		date1 = date.today().replace(day=1)
		date1 = str(date1.month) + '/' + str(date1.day) + '/' + str(date1.year)

		date2 = last_day_of_month(date.today())
		date2 = str(date2.month) + '/' + str(date2.day) +  '/' + str(date2.year)
		
		context ={
			"date1": date1,
			"date2":  date2,
		}
		return render(request, 'customers/accounting.html', context)



def export_orders(request):
    if request.method == 'POST':
        start = datetime.datetime.strptime(request.POST['start'], "%m/%d/%Y")
        end = datetime.datetime.strptime(request.POST['end'], "%m/%d/%Y")
        
        if start > end:
            context = {
                'error_message' : "Start date must be before end date!",
            }
            return render(request, 'customers/accounting.html', context)
        else:
            user_company= CompanyUser.objects.filter(user= request.user)
            item_sbu =[]
            if user_company :
                item_sbu = list(user_company.values_list('company', flat=True))

            completedorders = Order.objects.filter(date_ordered__gt=start).filter(date_ordered__lt=end).filter(complete = True).filter(company__in=item_sbu)
            allorders = Order.objects.filter(date_ordered__gt=start).filter(date_ordered__lt=end).filter(company__in=item_sbu)
            # expenses = Expense.objects.filter(date__gt=start).filter(date__lt=end).filter(company__in=item_sbu)
            
            # Sum of all paid invoices
            ordertotal = 0
            currencyTotals = {}
        

            for i in completedorders:
                valuetotal = i.total_price
                rate = i.currency.current_rate if i.currency else 1 #check syntax 16 Jan 2021
                
                ordertotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
                
                symbol = i.currency.symbol if i.currency else "USD"
                if symbol in currencyTotals:
                    currencyTotals[symbol] += i.total_price
                else:
                    currencyTotals[symbol] = i.total_price

        
            # Add invoice expenses within date range, regardless of invoice status
            
        
            response = HttpResponse(content_type='text/csv')
            # Name the csv file
            #transaction_id = str(datetime.datetime.now().timestamp())
            F ="{:0^2,d}"# 2---->02, 3--->03; etc
            Float_thousand ="{:,.2f}"# 2---->02, 3--->03; etc
            date_now = datetime.datetime.now() #date.today()
            date_now = str(date_now.year) + '_' + str(date_now.month) \
                      + '_' + str(date_now.day)+ "_" + str(date_now.hour) \
                        + '_' + str(date_now.minute) + "_" +  str(date_now.second)

            filename = "orders" + date_now +  ".csv"
            response['Content-Disposition'] = 'attachment; filename=' + filename
            writer = csv.writer(response, delimiter=',')
          

            # Writing the first row of the csv
            heading_text = "Orders" 
            writer.writerow([heading_text.upper(),"", "", start, end])
            writer.writerow(['Transaction ID', 'Name', 'Date Ordered','Complete', 'Company', 'Currency', 
                            'Total Value'])
            # Writing other rows
            for t in completedorders:
                writer.writerow([t.transaction_id, t.customer.name, t.date_ordered, t.complete,t.company.name, t.currency.symbol if t.currency else "" ,
                Float_thousand.format(t.total_price)])

            writer.writerow(["Total in USD", "", "", "","", "USD",
                Float_thousand.format(ordertotal)])
            
            writer.writerow(["totals in actual currencies" ])
           
            for item in currencyTotals.keys():
                writer.writerow(["","", "", "","", str(item) , str( Float_thousand.format(currencyTotals[item]))])
			
            # Return the response
            return response
    else:# default current month
        date1 = date.today().replace(day=1)
        date1 = str(date1.month) + '/' + str(date1.day) + '/' + str(date1.year)

        date2 = last_day_of_month(date.today())
        date2 = str(date2.month) + '/' + str(date2.day) +  '/' + str(date2.year)
        
        context ={
            "date1": date1,
            "date2":  date2,
        }
        return render(request, 'customers/export_orders.html', context)



def export_monthly_orders(request):
    F ="{:0^2,d}"# 2---->02, 3--->03; etc
    Float_thousand ="{:,.2f}"# 2---->02, 3--->03; etc
    user_company= CompanyUser.objects.filter(user= request.user)
    item_sbu =[]
    if user_company :
        item_sbu = list(user_company.values_list('company', flat=True))

    # initialise
    start_month = date.today() - relativedelta(months=5)
    first_day_of_current_month = start_month.replace(day=1)
    last_day_of_current_month = last_day_of_month(start_month)
    start = first_day_of_current_month

    MonthlySalesplan = {}
    MonthlyOrders = {}
    MonthlyPayments = {}
    MonthlyExpenses = {}
    MonthlyNetProfit= {}
    
    MonthlySalesplan["Month"]= "SalesPlans"
    MonthlyOrders["Month"]= "Orders"
    MonthlyPayments["Month"]= "Payments"
    MonthlyExpenses["Month"]= "Expenses"
    MonthlyNetProfit["Month"]= "Net Frofit"
    for i in range(6):
        end = last_day_of_current_month
        month_name = str(first_day_of_current_month.month) + " " + str(first_day_of_current_month.year)
  

        salesplanitems = SalesPlanItem.objects.filter(dstart__gte=first_day_of_current_month).filter(dend__lte=last_day_of_current_month).filter(salesplan__company__in=item_sbu)
        completedorders = Order.objects.filter(date_ordered__gt=first_day_of_current_month).filter(date_ordered__lt=last_day_of_current_month).filter(complete = True).filter(company__in=item_sbu)
        allinvoices = Invoice.objects.filter(date__gt=first_day_of_current_month).filter(date__lt=last_day_of_current_month).filter(company__in=item_sbu)
        paidinvoices = Invoice.objects.filter(date__gt=first_day_of_current_month).filter(date__lt=last_day_of_current_month).filter(status = 'Paid').filter(company__in=item_sbu)
        expenses = Expense.objects.filter(date__gt=first_day_of_current_month).filter(date__lt=last_day_of_current_month).filter(company__in=item_sbu)
        
    
        #--------------------SalesPlans---------------------------------------
        salestotal = 0
        for i in salesplanitems:
            valuetotal = i.qty *i.cost  # * i.product.price
            rate = i.salesplan.currency.current_rate if i.salesplan.currency else 1 
            
            salestotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
        
       
        if month_name in MonthlySalesplan:
            MonthlySalesplan[month_name] +=  Float_thousand.format(salestotal)
        else:
            MonthlySalesplan[month_name] =  Float_thousand.format(salestotal)

       #----------------------------------------------------------------------
        
        
        
        # Add invoice expenses within date range, regardless of invoice status
        for i in allinvoices:
            expenses = list(chain(expenses, Expense.objects.filter(invoice=i)))

        #--------------------Expenses----------------------------------------------------------
        expensetotal = 0
        for expense in expenses:
            if expense.currency is not None:
                expensetotal +=decimal.Decimal( expense.total()) / decimal.Decimal(expense.currency.current_rate)
            else :
                expensetotal += decimal.Decimal( expense.total()) / decimal.Decimal(expense.invoice.currency.current_rate)	
            
        
        if month_name in MonthlyExpenses:
            MonthlyExpenses[month_name] +=  Float_thousand.format(expensetotal)
        else:
            MonthlyExpenses[month_name] =  Float_thousand.format(expensetotal)

        #--------------------Paid Invoices----------------------------------------------------------
        invoicetotal = 0
        for i in paidinvoices:
            valuetotal = i.total_items()
            rate = i.currency.current_rate if i.currency else 1 
            
            invoicetotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
        
      
        if month_name in MonthlyPayments:
            MonthlyPayments[month_name] +=  Float_thousand.format(invoicetotal)
        else:
            MonthlyPayments[month_name] =  Float_thousand.format(invoicetotal)

      
        MonthlyNetProfit[month_name]=Float_thousand.format(invoicetotal-expensetotal)
        #--------------------Orders----------------------------------------------------------
        ordertotal = 0
        for i in completedorders:
            valuetotal = i.total_price
            rate = i.currency.current_rate if i.currency else 1 
            
            ordertotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
        
       
        if month_name in MonthlyOrders:
            MonthlyOrders[month_name] +=  Float_thousand.format(ordertotal)
        else:
            MonthlyOrders[month_name] =  Float_thousand.format(ordertotal)

       #----------------------------------------------------------------------
        # go back a month
        plus_1_months = last_day_of_current_month + relativedelta(months=1)
        first_day_of_current_month = plus_1_months.replace(day=1)
        last_day_of_current_month = last_day_of_month(plus_1_months)

    #end of period
    
    response = HttpResponse(content_type='text/csv')
    # Name the csv file
    #transaction_id = str(datetime.datetime.now().timestamp())
    
    date_now = datetime.datetime.now() #date.today()
    date_now = str(date_now.year) + '_' + str(date_now.month) \
                + '_' + str(date_now.day)+ "_" + str(date_now.hour) \
                + '_' + str(date_now.minute) + "_" +  str(date_now.second)

    filename = "Financial_Statement" + date_now +  ".csv"
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = csv.writer(response, delimiter=',')
    # Writing the first row of the csv
    heading_text = "Financial Statement" 
    writer.writerow([heading_text.upper(),"", "", start, end])
    
    
    #--Headings---
    writer.writerow([str(item) for item in MonthlySalesplan.keys()])
     #--- SalesPlans	
    writer.writerow([str(MonthlySalesplan[item]) for item in MonthlySalesplan.keys()])
    
   
    #--- Orders	
    writer.writerow([str(MonthlyOrders[item]) for item in MonthlyOrders.keys()])
    
    #--- Payments	
    writer.writerow([str(MonthlyPayments[item]) for item in MonthlyPayments.keys()])

    #--- Expenses	
    writer.writerow([str(MonthlyExpenses[item]) for item in MonthlyExpenses.keys()])

    #--- Net Profit	
    # writer.writerow([str(MonthlyPayments[item]-MonthlyExpenses[item]) for item in MonthlyPayments.keys()])
    writer.writerow([str(MonthlyNetProfit[item]) for item in MonthlyNetProfit.keys()])
    # Return the response
    return response




class ExportView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'customers/accounting_by_month.html'
    form_class = ExportForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form): 

        Float_thousand ="{:,.2f}"# 2---->02, 3--->03; etc
        item_sbu =form.cleaned_data['company']
        # initialise
        start_month = date.today() - relativedelta(months=5)
        first_day_of_current_month = start_month.replace(day=1)
        last_day_of_current_month = last_day_of_month(start_month)
        start = first_day_of_current_month

        MonthlySalesplan = {}
        MonthlyOrders = {}
        MonthlyPayments = {}
        MonthlyExpenses = {}
        MonthlyNetProfit= {}

        MonthlySalesplan["Month"]= "SalesPlans"
        MonthlyOrders["Month"]= "Orders"
        MonthlyPayments["Month"]= "Payments"
        MonthlyExpenses["Month"]= "Expenses"
        MonthlyNetProfit["Month"]= "Net Profit"
        for i in range(6):
            end = last_day_of_current_month
            month_name = str(short_month_name(first_day_of_current_month.month)) + " " + str(first_day_of_current_month.year)
            
            salesplanitems = SalesPlanItem.objects.filter(dstart__gte=first_day_of_current_month).filter(dend__lte=last_day_of_current_month).filter(salesplan__company__in=item_sbu)
        
            completedorders = Order.objects.filter(date_ordered__gt=first_day_of_current_month).filter(date_ordered__lt=last_day_of_current_month).filter(complete = True).filter(company__in=item_sbu)
            allinvoices = Invoice.objects.filter(date__gt=first_day_of_current_month).filter(date__lt=last_day_of_current_month).filter(company__in=item_sbu)
            paidinvoices = Invoice.objects.filter(date__gt=first_day_of_current_month).filter(date__lt=last_day_of_current_month).filter(status = 'Paid').filter(company__in=item_sbu)
            expenses = Expense.objects.filter(date__gt=first_day_of_current_month).filter(date__lt=last_day_of_current_month).filter(company__in=item_sbu)
            

            
            #--------------------SalesPlans---------------------------------------
            salestotal = 0
            for i in salesplanitems:
                valuetotal = i.qty *i.cost  # * i.product.price
                rate = i.salesplan.currency.current_rate if i.salesplan.currency else 1 
                
                salestotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
            
        
            if month_name in MonthlySalesplan:
                MonthlySalesplan[month_name] +=  Float_thousand.format(salestotal)
            else:
                MonthlySalesplan[month_name] =  Float_thousand.format(salestotal)

            #----------------------------------------------------------------------
            
            # Add invoice expenses within date range, regardless of invoice status
            for i in allinvoices:
                expenses = list(chain(expenses, Expense.objects.filter(invoice=i)))

            #--------------------Expenses----------------------------------------------------------
            expensetotal = 0
            for expense in expenses:
                if expense.currency is not None:
                    expensetotal +=decimal.Decimal( expense.total()) / decimal.Decimal(expense.currency.current_rate)
                else :
                    expensetotal += decimal.Decimal( expense.total()) / decimal.Decimal(expense.invoice.currency.current_rate)	
                
            
            if month_name in MonthlyExpenses:
                MonthlyExpenses[month_name] +=  Float_thousand.format(expensetotal)
            else:
                MonthlyExpenses[month_name] =  Float_thousand.format(expensetotal)

            #--------------------Paid Invoices----------------------------------------------------------
            invoicetotal = 0
            for i in paidinvoices:
                valuetotal = i.total_items()
                rate = i.currency.current_rate if i.currency else 1 
                
                invoicetotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
            
        
            if month_name in MonthlyPayments:
                MonthlyPayments[month_name] +=  Float_thousand.format(invoicetotal)
            else:
                MonthlyPayments[month_name] =  Float_thousand.format(invoicetotal)

        
            MonthlyNetProfit[month_name]=Float_thousand.format(invoicetotal-expensetotal)
            #--------------------Orders----------------------------------------------------------
            ordertotal = 0
            for i in completedorders:
                valuetotal = i.total_price
                rate = i.currency.current_rate if i.currency else 1 
                
                ordertotal += decimal.Decimal(valuetotal) /decimal.Decimal( rate) # decimal.Decimal(rate)
            
        
            if month_name in MonthlyOrders:
                MonthlyOrders[month_name] +=  Float_thousand.format(ordertotal)
            else:
                MonthlyOrders[month_name] =  Float_thousand.format(ordertotal)

        #----------------------------------------------------------------------
            # go back a month
            plus_1_months = last_day_of_current_month + relativedelta(months=1)
            first_day_of_current_month = plus_1_months.replace(day=1)
            last_day_of_current_month = last_day_of_month(plus_1_months)

        #end of period
        if form.cleaned_data['export_type']=="web":
          
            context ={
                "MonthlySalesplan": MonthlySalesplan,
                "MonthlyOrders": MonthlyOrders,
                "MonthlyPayments": MonthlyPayments,
                "MonthlyExpenses": MonthlyExpenses,
                "MonthlyNetProfit": MonthlyNetProfit,
                "Company_list": item_sbu,
                "web_view": True,
            }
            return render(self.request, 'customers/accounting_by_month.html', context)

        
        response = HttpResponse(content_type='text/csv')
        # Name the csv file
        #transaction_id = str(datetime.datetime.now().timestamp())
        
        date_now = datetime.datetime.now() #date.today()
        date_now = str(date_now.year) + '_' + str(date_now.month) \
                    + '_' + str(date_now.day)+ "_" + str(date_now.hour) \
                    + '_' + str(date_now.minute) + "_" +  str(date_now.second)

        filename = "Financial_Statement" + date_now +  ".csv"
        response['Content-Disposition'] = 'attachment; filename=' + filename
        writer = csv.writer(response, delimiter=',')
        # Writing the first row of the csv
        heading_text = "Financial Statement for period: " +  str(start) + " to " + str(end)
        writer.writerow([heading_text.upper()])
        
        #--Headings---
        writer.writerow([str(item) for item in MonthlySalesplan.keys()])
        #--- SalesPlans	
        writer.writerow([str(MonthlySalesplan[item]) for item in MonthlySalesplan.keys()])
      
        #--- Orders	
        writer.writerow([str(MonthlyOrders[item]) for item in MonthlyOrders.keys()])
        
        #--- Payments	
        writer.writerow([str(MonthlyPayments[item]) for item in MonthlyPayments.keys()])

        #--- Expenses	
        writer.writerow([str(MonthlyExpenses[item]) for item in MonthlyExpenses.keys()])

        #--- Net Profit	
        writer.writerow([str(MonthlyNetProfit[item]) for item in MonthlyNetProfit.keys()])

         #--- Company list
        #print(item_sbu) 
        company_str ="Company: "	
        for item in item_sbu:
            company_str += str(item) + "; " 	
        writer.writerow([company_str])
       	
        # writer.writerow([str(item) for item in item_sbu])
        # Return the response
        return response

@login_required(login_url="account_login")
def check_item(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            customer_id = request.POST['customer_id']
            if customer_id is not None :
                customer = get_object_or_404(Customer, pk=customer_id)
                order = Order.objects.filter(customer=customer, complete=False).first()
                data = {}
                data["status"]= False
                data["details"] = "" 
                if order :
                    data["details"]= "The customer " + str(customer.name)  + " has an uncompleted order dated "  + str(order.date_ordered)
                    data["status"]=True
                #print(data)
                return JsonResponse({'error': False, 'data': data})
            else:
                # print(createbookform.errors)
                return JsonResponse({'error': True, 'data': "errors encontered"})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'message': 'Record does not exist.'})
    return JsonResponse({'status': 'Fail', 'message': 'Error, must be an Ajax call.'})

