from django.shortcuts import render
from datetime import date, timedelta

from django.http import JsonResponse

from django.core.paginator import Paginator

from django.conf import settings

from django.views.generic import DetailView

import json

import datetime

from common.utils import get_current_user_groups
from investments_appraisal.models import UserPreference
from store.decorators import registered_user_only_with_client_routing
from .models import Customer, Company
from .models import *

from .filters import *

from .utils import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views import generic


import csv
import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from store import forms
#from . import importers
from . import models
#from rest_framework.authtoken.models import Token as AuthToken
#from common.utils import  get_invoice_total, get_expense_total
from .models import Invoice, Company, Expense
import pandas as pd

from datetime import date
import csv
from dateutil.relativedelta import relativedelta

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views import generic

from common.utils import last_day_of_month
from django.utils.decorators import method_decorator
#from store.decorators import unauthenticated_user, allowed_users, admin_only, \
#     registered_user_only_with_client_routing
from django.contrib.auth.decorators import login_required 

from django.template.loader import render_to_string

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from django.db.models.aggregates import Avg, Count, Max, Sum
from django.db.models import Q

 
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic


def product_load_tags_search_string(request, tagname, search_str):
    # replicate
  
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        customer = get_object_or_404(Customer, user=request.user)
        ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
       
        orderitems=None
        order=None
    else:
        ordermodel =None
        cookie_data = cookie_cart(request)
        #total_quantity = cookie_data['total_quantity']
        order = cookie_data['order']
        ordermodel = cookie_data['orderitems']

    tags= ProductCategory.objects.filter(name=tagname)
    models= Product.objects.filter(Q(tags__in=tags), Q(description__icontains=search_str))

    if not ('perpage' in request.session):
        #print('session[perpage] on set')
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6
    else:
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6


    per_page=request.session['perpage']
    obj_paginator = Paginator(models, per_page)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    
    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,        
        'current_page':current_page,
        'page_range':page_range,
        'search_tags':True,
        'slug':search_str,
        'tag_name':tagname,
        'tag_id':tags.first().id if tags.first() else "",
        'total_quantity': request.session['total_quantity'] if 'total_quantity' in request.session else '', 
        'ordermodel' : ordermodel
    }

    return render(request, 'store/store.html', context)

def product_load_tags(request, tag_id):
   
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        customer = get_object_or_404(Customer, user=request.user)
        ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
       
        orderitems=None
        order=None
    else:
        ordermodel =None
        cookie_data = cookie_cart(request)
        #total_quantity = cookie_data['total_quantity']
        order = cookie_data['order']
        ordermodel = cookie_data['orderitems']
       

    models= Product.objects.filter(Q(categories__in=tag_id))
    tag= get_object_or_404(ProductCategory,pk=tag_id)
    if not ('perpage' in request.session):
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6
    else:
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6


    per_page=request.session['perpage']
    obj_paginator = Paginator(models, per_page)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,        
        'current_page':current_page,
        'page_range':page_range,
        'search_tags':True,
        'tag_id':tag_id,
        'tag_name':tag.name,
        'total_quantity': request.session['total_quantity'] if 'total_quantity' in request.session else '', 
        'ordermodel' : ordermodel
    }

    return render(request, 'store/store.html', context)

#from store.lib import get_current_user_groups
def product_search_ajax(request,tag_id_or_slug, search_type,*args, **kwargs):
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        customer = get_object_or_404(Customer, user=request.user)
        ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems=None
        order=None
    else:
        ordermodel =None
        cookie_data = cookie_cart(request)
        #total_quantity = cookie_data['total_quantity']
        order = cookie_data['order']
        orderitems = cookie_data['orderitems']

    if request.method == 'POST':
        #description= request.POST['description']
        if search_type=='tags':
            # tags= Tag.objects.filter(name=slug)
            # print(slug, type(slug))
            modelsdata= Product.objects.filter(Q(categories__in=tag_id_or_slug))
        else:
            modelsdata= Product.objects.filter(Q(description__icontains=tag_id_or_slug))

        if not ('perpage' in request.session):
            if request.user.is_authenticated:
                obj= UserPreference.objects.filter(user=request.user).first()
                # anonymous user is not iterable
                if obj:
                    request.session['perpage']=obj.perpage
                else:# nothing in db
                    request.session['perpage']= 6
            else:
                request.session['perpage']= 6

        per_page=request.session['perpage']

        obj_paginator = Paginator(modelsdata, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        # range iterator of page numbers
        page_range = obj_paginator.page_range

        if request.is_ajax():
            #getting page number
            page_no = request.POST.get('page_no', None) 
            num_of_pages= int(obj_paginator.num_pages)
            totalrecords= int(obj_paginator.count)
            current_page = obj_paginator.get_page(page_no)    
            
            
            data={}	
            data["per_page"]=per_page
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

                if request.user.is_authenticated:
                    True_or_False, record=ordermodel.productIsInMyCart_2(i)

                else:
                    True_or_False=False
                    #locate appropriate orderitem
                    for j in orderitems:
                        if str(j['product']['id'])==str(i.id):
                            True_or_False=True
                            break    # break here 

                item_object['productIsInMyCart']=True_or_False
                
                categories=""
                for x in item_object['categories']:
                    categories = categories + str(x.name)  
                item_object['categories']=  categories
                if i.image:
                    item_object['image']= i.image.url
                else:
                    item_object['image']=None								 
                
                results.append(item_object)
                
            data["results"]=results
        
        return JsonResponse({"data":data})

def display_product_ajax(request):
    current_time = timezone.now()#datetime.datetime.now()
    models= Product.objects.all()#.order_by('-date')

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        customer = get_object_or_404(Customer, user=request.user)
        ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems=None
        order=None

    else:
        ordermodel =None
        cookie_data = cookie_cart(request)
        #total_quantity = cookie_data['total_quantity']
        order = cookie_data['order']
        orderitems = cookie_data['orderitems']


    if not ('perpage' in request.session):
        if request.user.is_authenticated:
                obj= UserPreference.objects.filter(user=request.user).first()
                # anonymous user is not iterable
                if obj:
                    request.session['perpage']=obj.perpage
                else:# nothing in db
                    request.session['perpage']= 6
        else:
            request.session['perpage']= 6
    else:
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6


    per_page=request.session['perpage']
    obj_paginator = Paginator(models, per_page)
    # list of objects on first page
    first_page = obj_paginator.page(1).object_list
    # range iterator of page numbers
    page_range = obj_paginator.page_range

   
    #
    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None) 
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
		
        current_page = obj_paginator.get_page(page_no)

            
        
        
        data={}	
        data["per_page"]=per_page
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
            if request.user.is_authenticated:
                True_or_False, record=ordermodel.productIsInMyCart_2(i)

            else:
                True_or_False=False
                #locate appropriate orderitem
                for j in orderitems:
                    if str(j['product']['id'])==str(i.id):
                        True_or_False=True
                        break    # break here 

            item_object['productIsInMyCart']=True_or_False
        
            categories=""
            for x in item_object['categories']:
                categories = categories + str(x.name)  
            item_object['categories']=  categories
            if i.image:
                item_object['image']= i.image.url
            else:
                item_object['image']=None
            results.append(item_object)	
        
        data["results"]=results
        
        
        return JsonResponse({"data":data})

def product_search_and_tags_ajax(request,tag_id, slug, search_type, *args, **kwargs):
    
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        customer = get_object_or_404(Customer, user=request.user)
        ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems=None
        order=None
    else:
        ordermodel =None
        cookie_data = cookie_cart(request)
        #total_quantity = cookie_data['total_quantity']
        order = cookie_data['order']
        orderitems = cookie_data['orderitems']

    if request.method == 'POST':
        if search_type == 1:
            modelsdata= Product.objects.filter(Q(categories__in=tag_id), Q(description__icontains=slug))
        else:
            modelsdata= Product.objects.filter(Q(categories__in=tag_id))
        
       

        if not ('perpage' in request.session):
            if request.user.is_authenticated:
                obj= UserPreference.objects.filter(user=request.user).first()
                # anonymous user is not iterable
                if obj:
                    request.session['perpage']=obj.perpage
                else:# nothing in db
                    request.session['perpage']= 6
            else:
                request.session['perpage']= 6

        per_page=request.session['perpage']

        obj_paginator = Paginator(modelsdata, per_page)
        # list of objects on first page
        first_page = obj_paginator.page(1).object_list
        # range iterator of page numbers
        page_range = obj_paginator.page_range

        if request.is_ajax():
            #getting page number
            page_no = request.POST.get('page_no', None) 
            num_of_pages= int(obj_paginator.num_pages)
            totalrecords= int(obj_paginator.count)
            current_page = obj_paginator.get_page(page_no)    
            
            
            data={}	
            data["per_page"]=per_page
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
                
                if request.user.is_authenticated:
                    True_or_False, record=ordermodel.productIsInMyCart_2(i)

                else:
                    True_or_False=False
                    #locate appropriate orderitem
                    for j in orderitems:
                        if str(j['product']['id'])==str(i.id):
                            True_or_False=True
                            break    # break here 

                item_object['productIsInMyCart']=True_or_False
                 
                categories=""
                for x in item_object['categories']:
                    categories = categories + str(x.name)  
                item_object['categories']=  categories
                if i.image:
                    item_object['image']= i.image.url
                else:
                    item_object['image']=None
                results.append(item_object)	
                    
            data["results"]=results
        
        return JsonResponse({"data":data})



class ExportView(LoginRequiredMixin, generic.edit.FormView):
    template_name = 'store/export.html'
    form_class = forms.ExportForm

    def form_valid(self, form):
        response = HttpResponse(content_type='text/csv')

        splits = models.Product.objects.date_range(
            form.cleaned_data['start'], form.cleaned_data['end']).transfers_once()
        splits = splits.filter(account__in=form.cleaned_data['accounts'])
        csv_writer = csv.writer(response, delimiter=';')
        headers = [
            'account',
            'opposing_account',
            'date',
            'amount',
            'category'
            ]
        csv_writer.writerow(headers)
        for split in splits.values_list('account__name', 'opposing_account__name',
                                        'date', 'amount', 'category__name'):
            csv_writer.writerow(split)

        response['Content-Disposition'] = 'attachment; filename=export.csv'
        return response

class ImportView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'store/import.html'

# class ProfileView(LoginRequiredMixin, generic.TemplateView):
#     template_name = 'store/profile.html'

#     def get_context_data(self, **kwargs):
#         context = super(ProfileView, self).get_context_data()
#         context['token'], created = AuthToken.objects.get_or_create(user=self.request.user)
#         return context



# ----our clients dont pass here but leapfrog to their page
@method_decorator(registered_user_only_with_client_routing(), name='dispatch')  
class IndexViewStartPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'store/index_startpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dstart = date.today().replace(day=1)
        dend = last_day_of_month(dstart)

        context['menu'] = 'charts'
        context['today'] = date.today()

        context['minus_3_months'] = date.today() - relativedelta(months=3)
        context['minus_6_months'] = date.today() - relativedelta(months=6)
        context['minus_12_months'] = date.today() - relativedelta(years=1)

        context['first_day_of_month'] = date.today().replace(day=1)
        context['last_day_of_month'] = last_day_of_month(date.today())
        

        company_df = pd.DataFrame(Company.objects.all().values())	
        sales_df = pd.DataFrame(Invoice.objects.all().values())
        expense_df = pd.DataFrame(Expense.objects.all().values())

       
        #print(expense_df)
        if sales_df.shape[0] > 0 and company_df.shape[0] > 0: 
            #at least one invoices made 
            # invoice is made against a company
            # only this condition suffice : with invoice the company is registered first
            # error was there at start of project when the database is empty
            company_df['company_id'] =company_df['id']
            df =pd.merge(company_df,sales_df, on='company_id').drop(['state','zip',
                    'email', 'street','date_created'], axis=1).rename(
                        {'id_x': 'id', 'id_y': 'invoice_id'}, axis=1)
            
            df['total'] = df['invoice_id'].apply(lambda x: get_invoice_total(x))
            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

            df['year'] = pd.to_datetime(df['date']).dt.year
            df['month'] = pd.to_datetime(df['date']).dt.month
            df['day'] = pd.to_datetime(df['date']).dt.day


            #this month
            date_filter =(df['date'] > str(dstart)) & (df['date'] < str(dend))
            df1 = df[date_filter]
        
            max_val = df1['total'].max()
            min_val = df1['total'].min()
            invoice_total_this_month = df1['total'].sum()
            aver_val = df1['total'].mean()

            expense_total_this_month = 0
            if expense_df.shape[0] > 0:
                expense_df['total'] = expense_df['id'].apply(lambda x: get_expense_total(x))
                expense_df['date'] = expense_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

                date_filter =(expense_df['date'] > str(dstart)) & (expense_df['date'] < str(dend))
                expense_df1 = expense_df[date_filter]
                expense_total_this_month = expense_df1['total'].sum()

            context['income'] = invoice_total_this_month
            context['expenses'] = expense_total_this_month
            context['difference'] =  context['income']- context['expenses']

            #--last month
            previous_last = dstart - timedelta(days=1)
            previous_first = previous_last.replace(day=1)

            #---this month
            date_filter =(df['date'] > str(previous_first)) & (df['date'] < str(previous_last))
            df2 = df[date_filter]
        
            # max_val = df2['total'].max()
            #min_val = df2['total'].min()
            invoice_total_last_month = df2['total'].sum()
            #aver_val = df2['total'].mean()
            
            expense_total_last_month=0
            if expense_df.shape[0]>0:

                date_filter =(expense_df['date'] > str(previous_first)) & (expense_df['date'] < str(previous_last))
                expense_df2 = expense_df[date_filter]
                expense_total_last_month = expense_df2['total'].sum()

        
            context['previous_income'] = invoice_total_last_month
            context['previous_expenses'] = expense_total_last_month
            context['previous_difference'] = context['previous_income']-  context['previous_expenses']
            context['today'] = date.today()
            context['last_month'] = previous_first
            context['past'] = date.today() - timedelta(days=60)

            user_group_set = get_current_user_groups(self.request.user)
            context['delete_key'] = True if 'admin' in user_group_set else False
            #any of two role
            context['edit_key'] = True if any(role in user_group_set for role in ('editor', 'admin')) else False
            context['admin_key'] = True if 'admin' in user_group_set else False
        return context


def search_filter_product(request):
    if request.method == 'GET':
        if request.is_ajax():
            # createbookform = BookModelForm(request.POST)
            #product_name = request.GET['product_name']
            #print(product_name)

            products = Product.objects.all().order_by('name')
            #print(request.GET)

            product_filter = ProductFilter(request.GET, queryset=products)
            #print(product_filter.qs)
            item_object ={}
            data = list(product_filter.qs.values())
            #print(data)
            item_object['product_filter'] = data
           
            paginated_product_filter = Paginator(product_filter.qs, 6)
            #print(paginated_product_filter)
            page_number = request.GET.get('page')
            product_page_obj = paginated_product_filter.get_page(page_number)
            
            
            
            item_object['product_page_obj'] = list(product_page_obj.values())
            #invoice_item_object['total_quantity'] = data['total_quantity']
            #print (item_object)
            return JsonResponse({'error': False, 'data': item_object})
        else:
            # print(createbookform.errors)
            return JsonResponse({'error': True, 'data': "errors encontered"})

    error = {
    'message': 'Error, must be an Ajax call.'
    }
    return JsonResponse(error, content_type="application/json")


def store(request):
    context = {}

    data = cart_data(request)
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        customer = get_object_or_404(Customer, user=request.user)
        ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
    else :
        ordermodel = None
        ordermodel =None
        cookie_data = cookie_cart(request)
        #total_quantity = cookie_data['total_quantity']
        ordermodel = cookie_data['order']
        ordermodel = cookie_data['orderitems']

    products = Product.objects.all().order_by('name')
    models= Product.objects.all().order_by('name')
    if not ('perpage' in request.session):
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6
    else:
        if request.user.is_authenticated:
            obj= UserPreference.objects.filter(user=request.user).first()
            # anonymous user is not iterable
            if obj:
                request.session['perpage']=obj.perpage
            else:# nothing in db
                request.session['perpage']= 6
        else:
            request.session['perpage']= 6


    per_page=request.session['perpage']
    # Paginator in a view function to paginate a queryset
    # show 4 news per page
    obj_paginator = Paginator(models, per_page)
    # list of objects on first page
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    # range iterator of page numbers
    page_range = obj_paginator.page_range

    request.session['total_quantity']=data['total_quantity']

    context['obj_paginator'] = obj_paginator
    context['first_page'] = first_page
    context['current_page'] = current_page
    context['page_range'] = page_range
    context['total_quantity'] = data['total_quantity']
    context['list_missing'] = [1,2]
    context['ordermodel']= ordermodel

    return render(request, 'store/store.html', context)
def store1(request):
    context = {}

    data = cart_data(request)

    #complex ranking of product
    # by though that have high turnover (sales)
    # promote products (induce shuffle to include product we intent to sales)
    # use AI for ranking
    # rank accorsing to user viewing our page, by region, race , customer segmatation
    # dated 06 March 2021 Andrew
    #print("inside main")
    products = Product.objects.all().order_by('name')
    #print(request.GET)

    product_filter = ProductFilter(request.GET, queryset=products)
    
    context['product_filter'] = product_filter
   # print(product_filter)
    paginated_product_filter = Paginator(product_filter.qs, 6)
   # print(paginated_product_filter)
    page_number = request.GET.get('page')
    product_page_obj = paginated_product_filter.get_page(page_number)
    
    #print(product_page_obj.object_list)
    # context['products'] = products
    context['product_page_obj'] = product_page_obj
    context['total_quantity'] = data['total_quantity']
    context['list_missing'] = [1,2]
    
    #print(data['total_quantity'])
    return render(request, 'store/store.html', context=context)


def cart(request):
    context = cart_data(request)

    return render(request, 'store/cart.html', context=context)


def checkout(request):
    context = cart_data(request)
    #not used anywhere
    #context['barikoi_autocomplete_api_key'] = settings.BARIKOI_AUTOCOMPLETE_API_KEY
    
    if request.user.is_authenticated:
        my_details = Customer.objects.get(user=request.user)

        if my_details:
            context['name']= my_details.name if my_details.name else ""
            context['email']= my_details.email if my_details.email else "" 
            context['address']= my_details.address1 if my_details.address1  else "" 
            context['city']= my_details.city if my_details.city  else "" 
            context['zip']= my_details.zip if my_details.zip else "" 

    return render(request, 'store/checkout.html', context=context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('action: ', action)
    print('product_id: ', product_id)

    #customer = request.user.customer
    customer = get_object_or_404(Customer, user=request.user)
    product = Product.objects.get(id=product_id)

    # get the latest order for this customer if none create
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Item was added.', safe=False)


def update_item_ajax(request):
    #
    if request.method == 'POST':
        product_id = request.POST.get('productId', None)
        action = request.POST.get('action', None)
        data={}
        if not (product_id == None or len(product_id)==0):
            #print('here......')
            #print(product_id)
            product = Product.objects.get(id=product_id)
            data["id"]= product.id
        else:
            #print('here22......')
            #print(product_id)
            data["deleted"]=True
            if request.user.is_authenticated:
                #customer = request.user.customer
                customer = get_object_or_404(Customer, user=request.user)
                #delete all null recors
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
                OrderItem.objects.filter(order=order, product__isnull=True).delete()
            else:
                pass
                #do this again


            data["o_total_price"]= order['total_price']
            data["o_total_qnty"]= order['total_quantity']
            data["id"]= product_id
            return JsonResponse({"data":data})
       
        

        if request.user.is_authenticated:
            #customer = request.user.customer
            customer = get_object_or_404(Customer, user=request.user)
            # get the latest order for this customer if none create
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                orderitem.quantity += 1
                #data["quantity"]=orderitem.quantity + 1
            elif action == 'remove':
                orderitem.quantity -= 1
                #data["quantity"]=orderitem.quantity + 1

            orderitem.save()

            if orderitem.quantity <= 0:
                orderitem.delete()
                data["deleted"]=True
                data["o_total_price"]= order.total_price
                data["o_total_qnty"]= order.total_quantity

            else:
                data["price"]= 0
                data["item"]= 0
                data["quantity"]= orderitem.quantity
                data["total"]= orderitem.total
                data["o_total_price"]= order.total_price
                data["o_total_qnty"]= order.total_quantity
        else:
            cookie_data = cookie_cart(request)
            #total_quantity = cookie_data['total_quantity']
            order = cookie_data['order']
            orderitems = cookie_data['orderitems']
            found=False
            #locate appropriate orderitem
            for i in orderitems:
                 if str(i['product']['id'])==str(product_id):
                    orderitem =i
                    found=True
                    break    # break here           

            if found==False:#object removed already
                data["deleted"]=True
                data["o_total_price"]= order['total_price']
                data["o_total_qnty"]= order['total_quantity']

            else:
                data["price"]= 0
                data["item"]= 0
                data["quantity"]= orderitem['quantity']
                data["total"]= orderitem['total']
                data["o_total_price"]= order['total_price']
                data["o_total_qnty"]= order['total_quantity']
        
        return JsonResponse({"data":data})


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        #---------worng----
        #customer = request.user.customer
        customer = get_object_or_404(Customer, user=request.user)
        print('>>>>>', customer)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #online purchasing by user dont provide company details
        if order.company is None:
            first_company = Company.objects.first()# default company
            order.company = first_company
           

    else:
        customer, order = guest_order(request, data)
        first_company = Company.objects.first()
        order.company = first_company

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # validate against actual price from the Order model
    # also check if cart is empty
    if (total == order.total_price) and (len(order.orderitem_set.all()) > 0):
        order.complete = True
    order.save()

    print('oder................', order)
    print("cus:................", customer)

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )

    #print('total: ', total)
    #print('order.total_price: ', order.total_price)
    #print('total == order.total_price: ', total == order.total_price)

    return JsonResponse('Payment complete.', safe=False)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'

    def get(self, request, pk) :
        context = {}

       
        if request.user.is_authenticated:
            customer, _ = Customer.objects.get_or_create(user=self.request.user)
            customer = get_object_or_404(Customer, user=self.request.user)
            ordermodel, created = Order.objects.get_or_create(customer=customer, complete=False)
            context['ordermodel'] = ordermodel
            orderitems=None
            order=None
        else:
            ordermodel =None
            cookie_data = cookie_cart(request)
            #total_quantity = cookie_data['total_quantity']
            order = cookie_data['order']
            orderitems = cookie_data['orderitems']
            context['ordermodel'] = orderitems

        product = Product.objects.get(id=pk)
        data = cart_data(request)
        context['total_quantity'] = data['total_quantity']
        context['product'] = product
        
        return render(request, self.template_name, context)