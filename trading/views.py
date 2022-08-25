import json
from datetime import date, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from dateutil.relativedelta import relativedelta
from common.decorators import admin_only
from django.contrib import messages
from common.utils import last_day_of_month
from investments_appraisal.models import ModelCategory, UserModel, UserPreference, UserProfile
from django.http import JsonResponse
from django.core.paginator import Paginator
from trading.db_filter import get_project_outputs_monthly
from trading.db_update import updateInvestorApplicationState
from django.urls import reverse
from trading.forms import InvestmentROIForm, InvestmentShareholdingForm, \
    InvestmentStrategyForm, InvestmentSummaryForm, InvestorForm, InvestorFormUpdate, \
    InvestorStatusUpdate, InvestorStatusUpdateAjax, ProjectOuputGraphPreferenceForm, UserInvestmentForm, UserInvestmentFormUpdate
from trading.reports import get_excel_investor_list
from .models import *
from django.db.models.expressions import F
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group

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

@login_required(login_url="account_login")
def get_user_businesses(request, type):
    BUSINESS_STATUS_CHOICE = ["unread","open","closed","all"] 
    current_time =timezone.now()# datetime.datetime.now()
      

    if type =="unread":
        queryset = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending') )
    elif type =="closed": 
        queryset = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time) )
    elif type =="open":
        queryset = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time))
    else:
       queryset = Investment.objects.filter(creater=request.user)
    
    total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
    sum_value=total_avg['sum']
    avg_value=total_avg['avg']
    if sum_value==None:
        sum_value=0
    if avg_value==None:
        avg_value=0  
    form = UserInvestmentForm(initial={'creater': request.user})
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
        "total_sum": sum_value,
        "average": round(avg_value,2)
    }
    return render(request, 'trading/user_businesses.html', context)


def business_search_and_tags_ajax(request,status, slug, search_type, *args, **kwargs):
    current_time =timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        if search_type == 1:
            if status =="unread":
                queryset = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending'), Q(description__icontains=slug) )
            elif status =="closed": 
                queryset = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time),  Q(description__icontains=slug))
            elif status =="open":
                queryset = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time), Q(description__icontains=slug))
            else:
                #allll
                queryset = Investment.objects.filter(Q(creater=request.user), Q(description__icontains=slug))
        else:
            if status =="unread":
                queryset = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending') )
            elif status =="closed": 
                queryset = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time) )
            elif status =="open":
                queryset = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time))
            else:
                #allll
                queryset = Investment.objects.filter(Q(creater=request.user))
        total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
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
            item_object['category']=i.category.name
            item_object['closing_date']=i.closing_date.ctime()
            item_object['date_created']=f'{i.date_created.ctime()}'
            item_object['current_investment']=i.current_investment
            item_object['user_stake']=i.userIsInvestorStake(request.user)
            item_object['current_investment_percent']=i.current_investment_percent 
            item_object['blogs_count']=i.blogs_count
            item_object['incoming_investors']=i.incoming_investors 
            item_object['user_investor']=i.userIsInvestorStatement(request.user)
            item_object['userIsOwner']=i.userIsOwner(request.user)
            item_object['user_investment_value']=i.userInvestorValue(request.user)
            item_object['user_investment_percent']=i.userInvestorPercent(request.user)
            item_object['investors_count']=i.investors_count                
            item_object['total_value']=i.total_value
            taglist = []
            for j in i.tags.all():
                taglist.append(j.name)
            item_object['tags']= taglist
            
            results.append(item_object)									 
        
            
        data["results"]=results
        data["total_sum"]=float(sum_value)
        data["average"]=float(round(avg_value,2))
        return JsonResponse({"data":data})
    else:
        return JsonResponse({'error': True, 'data': 'errors'})  
    

def investments_search_and_tags_ajax(request,status, slug, search_type, *args, **kwargs):
    current_time = timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        if search_type == 1:
            if status =="unread":
                queryset = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending'), Q(description__icontains=slug) )
            elif status =="closed": 
                queryset = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time),  Q(description__icontains=slug))
            elif status =="open":
                queryset = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time), Q(description__icontains=slug))
            else:
                #allll
                queryset = Investment.objects.filter(Q(creater=request.user), Q(description__icontains=slug))
        else:
            if status =="unread":
                queryset = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending') )
            elif status =="closed": 
                queryset = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time) )
            elif status =="open":
                queryset = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time))
            else:
                #allll
                queryset = Investment.objects.filter(Q(creater=request.user))
        
        total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
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
            item_object['category']=i.category.name
            item_object['closing_date']=i.closing_date.ctime()
            item_object['date_created']=f'{i.date_created.ctime()}'
            item_object['current_investment']=i.current_investment
            item_object['user_stake']=i.userIsInvestorStake(request.user)
            item_object['current_investment_percent']=i.current_investment_percent 
            item_object['blogs_count']=i.blogs_count
            item_object['incoming_investors']=i.incoming_investors 
            item_object['user_investor']=i.userIsInvestorStatement(request.user)
            item_object['userIsOwner']=i.userIsOwner(request.user)
            item_object['user_investment_value']=i.userInvestorValue(request.user)
            item_object['user_investment_percent']=i.userInvestorPercent(request.user)
            item_object['investors_count']=i.investors_count                
            item_object['total_value']=i.total_value
            taglist = []
            for j in i.tags.all():
                taglist.append(j.name)
            item_object['tags']= taglist
            
            results.append(item_object)									 
        
            
        data["results"]=results
        data["total_sum"]=float(sum_value)
        data["average"]=float(round(avg_value,2))
        return JsonResponse({"data":data})
    else:
        return JsonResponse({'error': True, 'data': 'errors'})  
 
def get_user_businesses_load_status_ajax(request,  status, *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            BUSINESS_STATUS_CHOICE = ["unread","open","closed","all"]
            current_time = timezone.now()#datetime.datetime.now() 
           
            if status =="unread":
                queryset = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending') )
            elif status =="closed": 
                queryset = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time) )
            elif status =="open":
                queryset = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time))
            else:
                #allll
                queryset = Investment.objects.filter(Q(creater=request.user))

            total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
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
                item_object['category']=i.category.name
                item_object['closing_date']=i.closing_date.ctime()
                item_object['date_created']=f'{i.date_created.ctime()}'
                item_object['current_investment']=i.current_investment
                item_object['user_stake']=i.userIsInvestorStake(request.user)
                item_object['current_investment_percent']=i.current_investment_percent 
                item_object['blogs_count']=i.blogs_count
                item_object['incoming_investors']=i.incoming_investors 
                item_object['user_investor']=i.userIsInvestorStatement(request.user)
                item_object['userIsOwner']=i.userIsOwner(request.user)
                item_object['user_investment_value']=i.userInvestorValue(request.user)
                item_object['user_investment_percent']=i.userInvestorPercent(request.user)
                item_object['investors_count']=i.investors_count                
                item_object['total_value']=i.total_value
                taglist = []
                for j in i.tags.all():
                    taglist.append(j.name)
                item_object['tags']= taglist
                
                results.append(item_object)									 
            
                
            data["results"]=results
            data["total_sum"]=float(sum_value)
            data["average"]=float(round(avg_value,2))
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})

@login_required(login_url="account_login")
def view_investors(request, id):
    investmet_obj = get_object_or_404(Investment,pk=id)    
    queryset=Investor.objects.filter(investment=investmet_obj) 
    #form = UserInvestmentForm(initial={'creater': request.user})
    context = {
        "models": queryset,
        "total": queryset.count(),
        "user": request.user,
        'investment':investmet_obj,
         'user_doc_name': investmet_obj.name
        #'form': form,
    }

    return render(request, 'trading/business_investors.html', context)

   

@login_required(login_url="account_login")
def get_user_investments_load_status(request, status):
    #this method is redundant: verify my assertion
    APLLICATION_STATUS_CHOICE = ["pending", "verification",  "accepted","engagement","rejected","all", "orphaned"]  
    queryset = Investor.objects.filter(Q(user=request.user)).first()  
  
    if status=='all':
        status=None
    df=queryset.trading_df_status(status)
    sum_total=0
    aver_val=0
    if len(df)>0 :
        df['id'] = pd.to_numeric(df.id)
   
        sum_total = df['myinvest'].sum()
        aver_val = df['myinvest'].mean()

    dict_,colms= dataframe_to_list_dict(df,True)
    #print(1, colms, dict_)
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
    

    #print(colms)
    obj_paginator = Paginator(dict_, pertable)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'current_page':current_page,
        'page_range':page_range,
        "user": request.user,
        "models": first_page,
        "total": len(dict_),
        'total_sum':sum_total,
        'average':aver_val,
        'search_status':True,
        'status':status,
        'APLLICATION_STATUS_CHOICE': APLLICATION_STATUS_CHOICE
    }

    return render(request, 'trading/user_investments.html', context)


def user_investments_search_and_tags_ajax(request,status, slug, search_type, *args, **kwargs):
    
  
    if request.method == 'POST':
        if request.is_ajax():
            APLLICATION_STATUS_CHOICE = ["pending", "verification","accepted","engagement", "rejected","all"]  
            queryset = Investor.objects.filter(Q(user=request.user)).first() 
            if status=='all':
                status=None
            if search_type != 1:
                slug =None     
            df=queryset.trading_df_status(status, slug)
            sum_total=0
            aver_val=0
            if len(df)>0 :
                df['id'] = pd.to_numeric(df.id)
        
                sum_total = df['myinvest'].sum()
                aver_val = df['myinvest'].mean()

            dict_,colms= dataframe_to_list_dict(df,True)
            #print(1, colms, dict_)
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
        

            #print(colms)
            obj_paginator = Paginator(dict_, pertable)
            first_page = obj_paginator.page(1).object_list
            current_page = obj_paginator.get_page(1)
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
        

            
            if int(1)>int(num_of_pages):			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]											 
            for i in obj_paginator.page(1).object_list:	
                item_object = {}
                for col_ in colms:
                    item_object[col_]=i[col_] 
                #----get the investment id----
                investment_id = i['iid']
                investment_obj= get_object_or_404(Investment, pk=investment_id)
                item_object['blogs_count']=investment_obj.blogs_count             
                results.append(item_object)
                
            data["results"]=results
            data["total_sum"]=float(sum_total)
            data["average"]=float(round(aver_val,2))
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})  

def get_accepted_investors_after_engagement_ajax(request,  id, *args, **kwargs):
   
    if request.method == 'POST':
        if request.is_ajax():
            APLLICATION_STATUS_CHOICE = ["pending",  "verification","accepted","engagement", "rejected","all"]  
            #queryset = Investor.objects.filter(Q(user=request.user),Q(investment__id__isnull=True)).first() 
         
            queryset = Investor.objects.filter(Q(user=request.user)).first() 
           
            #change selected accepted investor into engagement
            obj=Investor.objects.filter(user=request.user, investment__pk=id)
            obj= obj.first()
            if obj:
                obj.application_status= 'engagement'
                obj.date_status_changed= timezone.now()#datetime.datetime.now() 

                obj.save()

            df=queryset.trading_df_status('accepted')
            #aaaaaaaaaaaaaaaaaa
            #print(df.columns)
            #print(df)
            sum_total=0
            aver_val=0
            if len(df)>0 :
                df['id'] = pd.to_numeric(df.id)
        
                sum_total = df['myinvest'].sum()
                aver_val = df['myinvest'].mean()

            dict_,colms= dataframe_to_list_dict(df,True)
            #print(1, colms, dict_)
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
        

            #print(colms)
            obj_paginator = Paginator(dict_, pertable)
            first_page = obj_paginator.page(1).object_list
            current_page = obj_paginator.get_page(1)
            page_range = obj_paginator.page_range

            
            page_no = request.POST.get('page_no', None)
            if page_no== None:
                page_no=1 
           
            current_page = obj_paginator.get_page(page_no)    
            
            
          
            
            #page_no = request.POST.get('page_no', None) 
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
            queryset = Investor.objects.filter(Q(user=request.user),Q(application_status='accepted'))#    
            data["accepted"]=queryset.count() 

            #data["has_next"]=False
            if current_page.has_next():
                data["has_next"]=True  
                data["next_page_number"]=current_page.next_page_number()
            
            data["last"]=current_page.paginator.num_pages 
        

            
            if int(1)>int(num_of_pages):			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]											 
            for i in obj_paginator.page(1).object_list:	
                item_object = {}
                for col_ in colms:
                    item_object[col_]=i[col_] 
                #----get the investment id----
                investment_id = i['iid']
                investment_obj= get_object_or_404(Investment, pk=investment_id)
                item_object['blogs_count']=investment_obj.blogs_count             
                results.append(item_object)
                
            data["results"]=results

           
   
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})


def get_user_investments_load_status_ajax(request,  status, *args, **kwargs):
    #print('743:',status)
    if request.method == 'POST':
        if request.is_ajax():
            APLLICATION_STATUS_CHOICE = ["pending", "verification","accepted","engagement", "rejected","all" "orphaned"]  
            queryset = Investor.objects.filter(Q(user=request.user)).first() 
           
            if status=='all':
                status=None 
            df=queryset.trading_df_status(status)
            #print(df)
            sum_total=0
            aver_val=0
            if len(df)>0 :
                df['id'] = pd.to_numeric(df.id)
        
                sum_total = df['myinvest'].sum()
                aver_val = df['myinvest'].mean()

            dict_,colms= dataframe_to_list_dict(df,True)
            #print(1, colms, dict_)
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
        

            #print(colms)
            obj_paginator = Paginator(dict_, pertable)
            first_page = obj_paginator.page(1).object_list
            page_range = obj_paginator.page_range

            
            page_no = request.POST.get('page_no', None)
            if page_no== None:
                page_no=1 
           
            current_page = obj_paginator.get_page(page_no)    
            
            
          
            
            #page_no = request.POST.get('page_no', None) 
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
        

            
            if int(1)>int(num_of_pages):			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]											 
            for i in obj_paginator.page(page_no).object_list:	
                item_object = {}
                for col_ in colms:
                    item_object[col_]=i[col_] 
                #----get the investment id----
                investment_id = i['iid']
                investment_obj= get_object_or_404(Investment, pk=investment_id)
                item_object['blogs_count']=investment_obj.blogs_count             
                results.append(item_object)
                
            data["results"]=results
            data["total_sum"]=float(sum_total)
            data["average"]=float(round(aver_val,2))
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})

def get_user_investments_orphaned_ajax(request, *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            modeldata = Investor.objects.filter(Q(user=request.user),Q(investment__id__isnull=True)) 
            # avg_value= modeldata.aggregate(Avg('value'))['value__avg']
            # sum_value=modeldata.aggregate(models.Sum('value'))['value__sum']
            total_avg= modeldata.aggregate(sum=Sum('value'), avg=Avg('value'))
            sum_value=total_avg['sum']
            avg_value=total_avg['avg']
            if sum_value==None:
                sum_value=0
            if avg_value==None:
                avg_value=0  
            #print(total_avg['sum'],total_avg['avg'] )
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
        

            #print(colms)
            obj_paginator = Paginator(modeldata, pertable)
            first_page = obj_paginator.page(1).object_list
            page_range = obj_paginator.page_range

            
            page_no = request.POST.get('page_no', None)
            if page_no== None:
                page_no=1 
           
            current_page = obj_paginator.get_page(page_no)    
            
            
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
            
            if int(num_of_pages)==0:			
                data["results"]=[]
                return JsonResponse({"data":data})
            results=[]	
            # total_sum= 0
            # count =	0									 
            for i in obj_paginator.page(page_no).object_list:
                item_object = model_to_dict(i)
                # total_sum += item_object['value']
                # count +=1
                #print(total_sum)
                results.append(item_object)
                
            data["results"]=results
            data["total_sum"]=float(sum_value)
            data["average"]=float(round(avg_value,2))

            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})
@login_required(login_url="account_login")
def get_user_investments(request):
    APLLICATION_STATUS_CHOICE = ["pending", "verification","accepted","engagement", "rejected","all", "orphaned"]  
    queryset = Investor.objects.filter(user=request.user).first()  
    
    df=queryset.trading_df
    sum_total=0
    aver_val=0
    if len(df)>0 :
        df['id'] = pd.to_numeric(df.id)
   
        sum_total = df['myinvest'].sum()
        aver_val = df['myinvest'].mean()

    dict_,colms= dataframe_to_list_dict(df,True)
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
    

    #print(colms)
    obj_paginator = Paginator(dict_, pertable)
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    page_range = obj_paginator.page_range

    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        'current_page':current_page,
        'page_range':page_range,
        "user": request.user,
        "models": first_page,
        "total": len(dict_),
        'total_sum':sum_total,
        'average':aver_val,
        'status':'all',
        'APLLICATION_STATUS_CHOICE': APLLICATION_STATUS_CHOICE
    }

    return render(request, 'trading/user_investments.html', context)


def update_investment_likes_ajax(request,  id, *args, **kwargs):
    #obj = get_object_or_404(ModelCategory,id=id)
    obj = Investment.objects.filter(pk=id)
    if request.method == 'POST':
        if request.is_ajax():
            obj.update(likes=F('likes') + 1)		
            #obj.save()
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
            
        record = Investment.objects.get(pk=id)
        item_object = model_to_dict(record)
        taglist=[]
        for j in record.tags.all():
            taglist.append(j.name)
        item_object['tags']= taglist
        return JsonResponse({'error': False, 'data': item_object})
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})

def investment_search_and_tags_ajax(request,tag_id, slug, search_type, *args, **kwargs):
    current_time = timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        if search_type == 1:
            modelsdata= Investment.objects.filter(Q(closing_date__gte=current_time),Q(public=True), Q(tags__in=tag_id), Q(description__icontains=slug))
        else:
            modelsdata= Investment.objects.filter(Q(closing_date__gte=current_time), Q(public=True),Q(tags__in=tag_id))
        
        # total_avg= queryset.aggregate(sum=Sum('total_value'), avg=Avg('total_value'))
        # sum_value=total_avg['sum']
        # avg_value=total_avg['avg']

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
                item_object['closing_date']=i.closing_date.ctime()
                item_object['date_created']=f'new Date("{i.date_created.ctime()}")'
                item_object['date_created']=f'{i.date_created.ctime()}'
                item_object['uniqueid']=i.category.uniqueid
                True_or_False, record=i.userIsInvestor_2(request.user)
                item_object['userIsInvestor']=True_or_False
                if True_or_False ==True:
                    item_object['application_status']=record.application_status

                item_object['userIsOwner']=i.userIsOwner(request.user)
                item_object['user_investment_value']=i.userInvestorValue(request.user)
                item_object['user_investment_percent']=i.userInvestorPercent(request.user)
                item_object['current_investment_percent']=i.current_investment_percent
                item_object['blogs_count']=i.blogs_count
                 
                taglist = []
                for j in i.tags.all():
                    taglist.append(j.name)
                item_object['tags']= taglist
                results.append(item_object)
                
            data["results"]=results
        
        return JsonResponse({"data":data})


def investment_search_ajax(request,tag_id_or_slug, search_type,*args, **kwargs):
    current_time = timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        #description= request.POST['description']
        if search_type=='tags':
            # tags= Tag.objects.filter(name=slug)
            # print(slug, type(slug))
            modelsdata= Investment.objects.filter(Q(closing_date__gte=current_time), Q(tags__in=tag_id_or_slug), Q(public=True))
        else:
            modelsdata= Investment.objects.filter(Q(closing_date__gte=current_time), Q(description__icontains=tag_id_or_slug), Q(public=True))

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
                item_object['closing_date']=i.closing_date.ctime()
                item_object['date_created']=f'new Date("{i.date_created.ctime()}")'
                item_object['date_created']=f'{i.date_created.ctime()}'
                item_object['uniqueid']=i.category.uniqueid
                
               

                True_or_False, record=i.userIsInvestor_2(request.user)
                item_object['userIsInvestor']=True_or_False
                if True_or_False ==True:
                    item_object['application_status']=record.application_status

                item_object['userIsOwner']=i.userIsOwner(request.user)
                item_object['user_investment_value']=i.userInvestorValue(request.user)
                item_object['user_investment_percent']=i.userInvestorPercent(request.user)
                item_object['current_investment_percent']=i.current_investment_percent 
                item_object['blogs_count']=i.blogs_count
                taglist = []
                for j in i.tags.all():
                    taglist.append(j.name)
                item_object['tags']= taglist
                results.append(item_object)
                
            data["results"]=results
        
        return JsonResponse({"data":data})

def display_investment_ajax(request):
    current_time = timezone.now()#datetime.datetime.now()
    models= Investment.objects.filter(Q(closing_date__gte=current_time),Q(public=True))#.order_by('-date')


    if not ('perpage' in request.session):
        #print('session[perpage] on set')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
    else:
        #print('2. session[perpage] is...')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('2.userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
        #print('2. session[perpage] =', request.session['perpage'])


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
            item_object['closing_date']=i.closing_date.ctime()
            item_object['date_created']=f'new Date("{i.date_created.ctime()}")'
            item_object['date_created']=f'{i.date_created.ctime()}'
            item_object['uniqueid']=i.category.uniqueid
            True_or_False, record=i.userIsInvestor_2(request.user)
            item_object['userIsInvestor']=True_or_False
            if True_or_False ==True:
                item_object['application_status']=record.application_status
            item_object['userIsOwner']=i.userIsOwner(request.user)
            item_object['user_investment_value']=i.userInvestorValue(request.user)
            item_object['user_investment_percent']=i.userInvestorPercent(request.user)
            item_object['current_investment_percent']=i.current_investment_percent 
            item_object['blogs_count']=i.blogs_count
            taglist = []
            for j in i.tags.all():
                taglist.append(j.name)
            item_object['tags']= taglist
            results.append(item_object)
        
        data["results"]=results
        
        
        return JsonResponse({"data":data})


        
def update_view_on_view(request,id):
	obj = Investment.objects.filter(pk=id)
	obj.update(views=F('views') + 1)


@login_required
def investment_details(request,id):
    #update views before display... this view is included... there is no sero views
    update_view_on_view(request,id)
    investmet_obj = get_object_or_404(Investment,pk=id)
    
    id =investmet_obj.id
    is_user_investor=False
    investor_id=1
    obj=Investor.objects.filter(user=request.user, investment=investmet_obj) 
    if obj.first():
        is_user_investor=True
        investor_id=obj.first().id

 
    form = InvestorForm(initial={'user': request.user, 'investment': investmet_obj})


        #4. Model Taxes
    invest_details = InvestmentDetails.objects.filter(investment=investmet_obj).first()
    if invest_details :	
        investment_summary_form = InvestmentSummaryForm(instance=invest_details)
        investment_strategy_form = InvestmentStrategyForm(instance=invest_details)
        investment_shareholding_form = InvestmentShareholdingForm(instance=invest_details)
        investment_roi_form = InvestmentROIForm(instance=invest_details)
    else:
        investment_summary_form = InvestmentSummaryForm(initial={'investment': investmet_obj})	
        investment_strategy_form = InvestmentStrategyForm(initial={'investment': investmet_obj})
        investment_shareholding_form = InvestmentShareholdingForm(initial={'investment': investmet_obj})	
        investment_roi_form = InvestmentROIForm(initial={'investment': investmet_obj})	

    context = {
        'model':investmet_obj,
        "is_user_investor": is_user_investor,
        "is_user_record_owner": True if investmet_obj.creater == request.user else False,
        'first_entry': True,
        "user": request.user,
        'form': form,
        'investor_id': investor_id,
        "investment_details": invest_details,
        "investment_summary_form": investment_summary_form,
        "investment_strategy_form": investment_strategy_form,
        "investment_shareholding_form": investment_shareholding_form,
        'investment_roi_form': investment_roi_form,
    }
    return render(request, 'trading/investment-details.html', context)


@login_required
def investor_details(request,id, investment_id):
    
    # limit investment to my own ONLY: avoid other users accessing private data
    investment_obj = get_object_or_404(Investment,pk=investment_id,creater=request.user)
    #only investors of current investments
    investor_obj = get_object_or_404(Investor,pk=id, investment=investment_obj)
    if investor_obj.application_status =='pending':
        investor_obj.application_status ='verification'
        investor_obj.date_status_changed=timezone.now()# datetime.datetime.now()
        investor_obj.save()
        changed_to_verification=True
        messages.success(request, "Application state as been changed from pending to verification")
  
    userprofile_obj = get_object_or_404(UserProfile,user=investor_obj.user)

    form = InvestorStatusUpdate(instance=investor_obj,user=request.user)

    context = {
        'model':investor_obj,
        'investment':investment_obj,
        'userprofile':userprofile_obj,
        'form':form
    }
    return render(request, 'trading/investor-details.html', context)

       
@login_required
def edit_investment(request,id):
    #editing limited to owner of the investment only....
   
    #throws an error if user is invalid.....
    investmet_obj = get_object_or_404(Investment,pk=id, creater=request.user)
    id =investmet_obj.id
    is_user_investor=False
    investor_id=1
    obj=Investor.objects.filter(user=request.user, investment=investmet_obj) 
    #print('chck.....')
    if obj.first():
        #print('.....Found',obj.first() )
        is_user_investor=True
        investor_id=obj.first().id

   
    form = InvestorForm(initial={'user': request.user, 'investment': investmet_obj})


        #4. Model Taxes
    invest_details = InvestmentDetails.objects.filter(investment=investmet_obj).first()
    if invest_details :	
        investment_summary_form = InvestmentSummaryForm(instance=invest_details)
        investment_strategy_form = InvestmentStrategyForm(instance=invest_details)
        investment_shareholding_form = InvestmentShareholdingForm(instance=invest_details)
        investment_roi_form = InvestmentROIForm(instance=invest_details)
    else:
        investment_summary_form = InvestmentSummaryForm(initial={'investment': investmet_obj})	
        investment_strategy_form = InvestmentStrategyForm(initial={'investment': investmet_obj})
        investment_shareholding_form = InvestmentShareholdingForm(initial={'investment': investmet_obj})	
        investment_roi_form = InvestmentROIForm(initial={'investment': investmet_obj})	

    context = {
        'model':investmet_obj,
        'investment_id':id,
        "is_user_investor": is_user_investor,
        "is_user_record_owner": True if investmet_obj.creater == request.user else False,
        'first_entry': False,
        "user": request.user,
        'form': form,
        'investor_id': investor_id,
        "investment_details": invest_details,
        "investment_summary_form": investment_summary_form,
        "investment_strategy_form": investment_strategy_form,
        "investment_shareholding_form": investment_shareholding_form,
        'investment_roi_form': investment_roi_form,
    }
    return render(request, 'trading/edit-investment.html', context)

@login_required
def home(request):
    current_time = timezone.now()#datetime.datetime.now()
    models= Investment.objects.filter(Q(closing_date__gte=current_time), Q(public=True))
    if not ('perpage' in request.session):
        #print('session[perpage] on set')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
    else:
        #print('2. session[perpage] is...')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('2.userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
        #print('2. session[perpage] =', request.session['perpage'])


    per_page=request.session['perpage']
    # Paginator in a view function to paginate a queryset
    # show 4 news per page
    obj_paginator = Paginator(models, per_page)
    # list of objects on first page
    first_page = obj_paginator.page(1).object_list
    current_page = obj_paginator.get_page(1)
    # range iterator of page numbers
    page_range = obj_paginator.page_range



    context = {
        'obj_paginator':obj_paginator,
        'first_page':first_page,
        
        'current_page':current_page,
        'page_range':page_range
    }

    return render(request, 'trading/trading.html', context)

@login_required
def investment_load_tags_search_string(request, tagname, search_str):
    # replicate
    #print(tagname, search_str) 
    tags= Tag.objects.filter(name=tagname)
    current_time = timezone.now()#datetime.datetime.now()
    models= Investment.objects.filter(Q(closing_date__gte=current_time),Q(public=True), Q(tags__in=tags), Q(description__icontains=search_str))

    if not ('perpage' in request.session):
        #print('session[perpage] on set')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
    else:
        #print('2. session[perpage] is...')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('2.userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
        #print('2. session[perpage] =', request.session['perpage'])


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
    }

    return render(request, 'trading/trading.html', context)
@login_required
def investment_load_tags(request, tag_id):
    current_time = timezone.now()#datetime.datetime.now()
    models= Investment.objects.filter(Q(tags__in=tag_id), Q(public=True), Q(closing_date__gte=current_time))
    tag= get_object_or_404(Tag,pk=tag_id)
    if not ('perpage' in request.session):
        #print('session[perpage] on set')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
    else:
        #print('2. session[perpage] is...')
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            #print('2.userpref found')
            request.session['perpage']=obj.perpage
        else:# nothing in db
            request.session['perpage']= 6
        #print('2. session[perpage] =', request.session['perpage'])


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
        'tag_name':tag.name
    }

    return render(request, 'trading/trading.html', context)
def project_details(request,id):
	#model= ModelCategory.objects.filter(pk=id)
	model = get_object_or_404(Investment,pk=id)
	
	context ={'model':model}
	return render(request, 'trading/home.html', context)




login_required(login_url="account_login")
def create_userinvestment_ajax(request):
	if request.method == 'POST':
		form = UserInvestmentForm(data=request.POST or None)
	else:
		#first time call from loco failure list
		form = UserInvestmentForm(initial={'user': request.user})
	return create_all_useinvestment(request,form,'trading/user_investment_modal.html')


login_required(login_url="account_login")
def create_all_useinvestment(request,form,template_name):

    data = dict()
    errors= None
    if request.method == 'POST':
        errors=form.errors
        
        if form.is_valid():
            form.save()
            #total_pages= get_total_pages(request)
            data['form_is_valid'] = True
            latest = Investment.objects.latest('id').id
            record = Investment.objects.get(pk=latest)
            item_object = model_to_dict(record)
            taglist=[]
            for j in record.tags.all():
                taglist.append(j.name)
            item_object['tags'] =taglist
            data['model'] = item_object
            #data['total_pages']=total_pages
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


login_required(login_url="account_login")
def userinvestor_update_ajax(request,pk):
	investor = get_object_or_404(Investor,pk=pk)
	if request.method == 'POST':
		form = InvestorFormUpdate(request.POST or None, 
										instance=investor)
	else:
		#first time call from loco failure list
		form = InvestorFormUpdate( instance=investor)
	return save_all_user_investor_update(request,form,'trading/user_investor_edit_modal.html')


def save_all_user_investor_update(request,form,template_name):

    data = dict()
    errors= None
    # retrieve product
    pk = form.instance.id
    item_instance = get_object_or_404(Investor,pk=pk)
    if request.method == 'POST':
        # retrieve product
        pk = form.instance.id
        item_instance = get_object_or_404(Investor,pk=pk)
        #eject errors for modal form display
        errors=form.errors
        if form.is_valid():            
                form.save()
                pk = form.instance.id
                item_instance = get_object_or_404(Investor,pk=pk)
                data['form_is_valid'] = True
                item_object = model_to_dict(item_instance)
                parent_invest = Investment.objects.filter(investor=item_instance).first()
                if parent_invest:
                    item_object['current_investment']=parent_invest.current_investment
                    item_object['user_stake']=parent_invest.userIsInvestorStake(request.user)
                    
                    item_object['current_investment_percent']=parent_invest.current_investment_percent
                    item_object['incoming_investors']=parent_invest.incoming_investors
                    item_object['user_investor']=parent_invest.userIsInvestorStatement(request.user)
                    data['is_user_investor_bool']=parent_invest.userIsInvestor(request.user)
                    item_object['user_investment_value']=parent_invest.userInvestorValue(request.user)
                    item_object['user_investment_percent']=parent_invest.userInvestorPercent(request.user)
                    item_object['userIsOwner']=parent_invest.userIsOwner(request.user)
                    
                    item_object['investors_count']=parent_invest.investors_count
                    item_object['blogs_count']=parent_invest.blogs_count
                item_object['investor_id']=pk
                item_object['total_value']=parent_invest.total_value

                
                data['model'] = item_object
        else:
        
            data['form_is_valid'] = False
    else:
        parent_invest = Investment.objects.filter(investor=item_instance).first()
        if parent_invest:
            data['is_user_investor_bool']=parent_invest.userIsInvestor(request.user)
        

    context = {
        'form':form,
        'usermodel':item_instance,
    }

    data['html_form'] = render_to_string(template_name,context,request=request)
    data['error']= errors
    data['user_is_owner']= request.user ==item_instance.investment.creater
    data['total_value']= item_instance.investment.total_value
    data['value']= item_instance.value

    
    return JsonResponse(data)


login_required(login_url="account_login")
def create_userbusiness_ajax(request):
	if request.method == 'POST':
		form = UserInvestmentForm(data=request.POST or None)
	else:
		#first time call from loco failure list
		form = UserInvestmentForm(initial={'user': request.user})
	return create_all_user_business(request,form,'trading/user_business_modal.html')


login_required(login_url="account_login")
def create_all_user_business(request,form,template_name):

    data = dict()
    errors= None
    if request.method == 'POST':
        errors=form.errors
        
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            latest = Investment.objects.latest('id').id
            record = Investment.objects.get(pk=latest)
            item_object = model_to_dict(record)
            item_object['category']=record.category.name
            item_object['creater']=record.creater.username 
            item_object['current_investment']= record.current_investment 
            item_object['user_stake']=record.userIsInvestorStake(request.user)
            item_object['user_investor']=record.userIsInvestorStatement(request.user)
            item_object['userIsOwner']=record.userIsOwner(request.user)
            item_object['user_investment_value']=record.userInvestorValue(request.user)
            item_object['user_investment_percent']=record.userInvestorPercent(request.user)
            item_object['current_investment_percent']=record.current_investment_percent
            item_object['blogs_count']=record.blogs_count
            item_object['incoming_investors']=record.incoming_investors        
            item_object['investors_count']= record.investors_count
            item_object['total_value']=record.total_value
            item_object['date_created']= record.date_created.ctime()
            item_object['closing_date']=record.closing_date.ctime()
            taglist = []
            for i in record.tags.all():
                   taglist.append(i.name)
            item_object['tags']= taglist
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


login_required(login_url="account_login")
def create_userinvestor_ajax(request):
	if request.method == 'POST':
		form = InvestorForm(data=request.POST or None)
	else:
		#first time call from loco failure list
		form = InvestorForm(initial={'user': request.user})
	return create_all_user_investor(request,form,'trading/user_investor_modal.html')


login_required(login_url="account_login")
def create_all_user_investor(request,form,template_name):

    data = dict()
    errors= None
    if request.method == 'POST':
        errors=form.errors
        
        if form.is_valid():
            form.save()
            #total_pages= get_total_pages(request)
            data['form_is_valid'] = True
            latest = Investor.objects.latest('id').id
            record = Investor.objects.get(pk=latest)
            item_object = model_to_dict(record)
            parent_invest = Investment.objects.filter(investor=record).first()
            if parent_invest:
                item_object['current_investment']=parent_invest.current_investment 
                item_object['user_stake']=parent_invest.userIsInvestorStake(request.user)
                item_object['user_investor']=parent_invest.userIsInvestorStatement(request.user)
                item_object['userIsOwner']=parent_invest.userIsOwner(request.user)
                item_object['user_investment_value']=parent_invest.userInvestorValue(request.user)
                item_object['user_investment_percent']=parent_invest.userInvestorPercent(request.user)
                item_object['current_investment_percent']=parent_invest.current_investment_percent
                item_object['blogs_count']=parent_invest.blogs_count
                item_object['incoming_investors']=parent_invest.incoming_investors    
                item_object['investors_count']=parent_invest.investors_count
                item_object['total_value']=parent_invest.total_value
            item_object['investor_id']=latest



            data['model'] = item_object
            #data['total_pages']=total_pages
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


def dataframe_to_list_dict(df, isDataFrame):
    lst=[]
    output_list =[]
    columns_list=[]
    df_col_list=[]
    # if none empty merged df
    if isDataFrame:
        lst = df.values.tolist()
        index_lst=df.index.tolist()
        
        df_col_list = df.columns
        columns_list = df_col_list.tolist()
   
    
    
    item_counter = 1
    
    for i_record in lst:
        #new per each record...
        #print(i_record)
        record_dict = {}
        record_dict['item']= item_counter
        record_dict['index']= index_lst[item_counter-1]

        #--- each row makes a dict of cols-----
        for k in range(len(df_col_list)):
            col_name = df_col_list[k]          
            if col_name =='id':
                #change to integer
                record_dict[col_name]=int(i_record[k])
            else:
                record_dict[col_name]=i_record[k]
       
        item_counter +=1 
        output_list.append(record_dict)
    return output_list, columns_list

@login_required(login_url="account_login")
def delete_investor_this_user_ajax(request, investment_id, *args, **kwargs):
    
    if request.method == 'POST':
        #print(request.POST)
        if request.is_ajax():
            investment = get_object_or_404(Investment, pk=investment_id)

            model_ = get_object_or_404(Investor, user=request.user, investment=investment)

            model_.delete()
            #refreshed
            i = get_object_or_404(Investment, pk=investment_id)

            cdate= i.date_created.ctime()
            item_object = model_to_dict(i)
            item_object['closing_date']=i.closing_date.ctime()
            item_object['date_created']=f'new Date("{i.date_created.ctime()}")'
            item_object['date_created']=f'{i.date_created.ctime()}'
            item_object['uniqueid']=i.category.uniqueid
            True_or_False, record=i.userIsInvestor_2(request.user)
            item_object['userIsInvestor']=True_or_False
            if True_or_False ==True:
                item_object['application_status']=record.application_status
            item_object['userIsOwner']=i.userIsOwner(request.user)
            item_object['current_investment_percent']=i.current_investment_percent
            item_object['blogs_count']=i.blogs_count
            #print('**********', item_object)
            taglist = []
            for j in i.tags.all():
                taglist.append(j.name)
            item_object['tags']= taglist
            #print(item_object)

            data= {}
         

            #print(item_object)
            data['model']=item_object
            
            return JsonResponse({'error': False, 'data': data})
            
        else:
            return JsonResponse({'error': True, 'data': "errors encontered"})
    else:
        error = {
            'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json")

@login_required(login_url="account_login")
def delete_investor_ajax(request, id, page_no, *args, **kwargs):
   
    if request.method == 'POST':
        #print(request.POST)
        if request.is_ajax():
            
            model_ = get_object_or_404(Investor, pk=id)
            invest_id =None
            if model_.investment:
                invest_id= model_.investment.id
          
            item_object = model_to_dict(model_)
            model_.delete()
            
            item_instance =None
            if invest_id:
                item_instance = get_object_or_404(Investment,pk=invest_id)
           
            total_pages= get_total_pages_dict(request)
            data= {}
            data['total_pages']=total_pages
            data['deleted_page']=page_no
            
           
            
            queryset = Investor.objects.filter(user=request.user).first()  
            #print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWw3')
            df=queryset.trading_df
            sum_total=0
            aver_val=0
            if len(df)>0 :
                df['id'] = pd.to_numeric(df.id)
        
                sum_total = df['myinvest'].sum()
                aver_val = df['myinvest'].mean()
            item_object['total_sum']=int(sum_total)
            item_object['average']=round(aver_val,2)
            item_object['investor_id']=id
            if item_instance:
                item_object['current_investment']=item_instance.current_investment
                item_object['user_investment_percent']=item_instance.userInvestorPercent(request.user)
                item_object['current_investment_percent']=item_instance.current_investment_percent            
            

            #print('>>>>>>>>', item_object)
            data['model']=item_object
            
            return JsonResponse({'error': False, 'data': data})
            
        else:
            return JsonResponse({'error': True, 'data': "errors encontered"})
    else:
        error = {
            'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json")

@login_required(login_url="account_login")
def delete_investment_ajax(request, id,page_no, *args, **kwargs):
    if request.method == 'POST':
        #print(request.POST)
        if request.is_ajax():
            
            model_ = get_object_or_404(Investment, pk=id)

            model_.delete()
            item_object = model_to_dict(model_)

            total_pages= get_total_pages(request)
            data= {}
            data['total_pages']=total_pages
            data['deleted_page']=page_no
            taglist=[]
            # for j in model_.tags.all():
            #     taglist.append(j.name)
            # aaaa
            item_object['tags'] =[]#taglist 
            data['model']=item_object

            #print('..........', item_object)
            #messages.success(request, "Successfully deleted  model")
            
            return JsonResponse({'error': False, 'data': data})
            
        else:
            return JsonResponse({'error': True, 'data': "errors encontered"})
    else:
        error = {
            'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json")


def get_total_pages(request):
	if not ('pertable' in request.session):
		obj= UserPreference.objects.filter(user=request.user).first()
		if obj:
			request.session['pertable']=obj.pertable
		else:# nothing in db
			request.session['pertable']= 3
	pertable=request.session['pertable']
	#per_page=request.session['pertable']
	recordcount= Investment.objects.filter(creater=request.user).count()
	#avoide error
	if pertable==0:
		pertable=10
	return math.ceil(recordcount/pertable)

def get_total_pages_dict(request):
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 10
    pertable=request.session['pertable']

    queryset = Investor.objects.filter(user=request.user).first()  
    df=queryset.trading_df
    
    if len(df)>0 :
        df['id'] = pd.to_numeric(df.id)

    dict_, _= dataframe_to_list_dict(df,True)

    recordcount= len(dict_)
    #avoide error
    if pertable==0:
        pertable=10
    return math.ceil(recordcount/pertable)

login_required(login_url="account_login")
def update_investment_ajax(request,pk):
    user_invest = get_object_or_404(Investment,pk=pk)
    if request.method == 'POST':
        form = UserInvestmentFormUpdate(request.POST or None, 
                                        instance=user_invest)
    else:
        form = UserInvestmentFormUpdate( instance=user_invest)

   
    return save_all_user_investment(request,form,'trading/user_investment_edit_modal.html')



def save_all_user_investment(request,form,template_name):

    data = dict()
    errors= None
    # retrieve product
    pk = form.instance.id
    item_instance = get_object_or_404(Investment,pk=pk)
    if request.method == 'POST':
        # retrieve product
        pk = form.instance.id
        
        #eject errors for modal form display
        errors=form.errors
        if form.is_valid():			
            form.save()
            pk = form.instance.id
           
            item_instance = get_object_or_404(Investment,pk=pk)
            data['form_is_valid'] = True
            item_object = model_to_dict(item_instance)
            item_object['category']=item_instance.category.name
            item_object['creater']=item_instance.creater.username
            item_object['closing_date']=item_instance.closing_date.ctime()
            item_object['date_created']=item_instance.date_created.ctime()
            item_object['current_investment']=item_instance.current_investment
            item_object['user_stake']=item_instance.userIsInvestorStake(request.user)
            item_object['user_investor']=item_instance.userIsInvestorStatement(request.user)
            item_object['userIsOwner']=item_instance.userIsOwner(request.user)
            item_object['user_investment_value']=item_instance.userInvestorValue(request.user)
            item_object['user_investment_percent']=item_instance.userInvestorPercent(request.user)
            item_object['current_investment_percent']=item_instance.current_investment_percent            
            item_object['blogs_count']=item_instance.blogs_count
            item_object['incoming_investors']=item_instance.incoming_investors
            item_object['investors_count']=item_instance.investors_count                
            item_object['total_value']=item_instance.total_value
            item_object['closed_status']=item_instance.closed_status
            
            taglist = []
            for i in item_instance.tags.all():
                   taglist.append(i.name)
            item_object['tags']= taglist
            #print(item_object)
            data['model'] = item_object
        else:
        
            data['form_is_valid'] = False

    context = {
        'form':form,
        'usermodel':item_instance,
    }

    data['html_form'] = render_to_string(template_name,context,request=request)
    data['error']= errors
    return JsonResponse(data)


@login_required(login_url="account_login")
def edit_model_investment_paragraph_ajax(request, id, *args, **kwargs):
    if request.method == 'POST':
        #print(request.POST)
        if request.is_ajax():
            _instance = get_object_or_404(InvestmentDetails, pk=id)
            try:
                for i in request.POST:
                    if i=='summary':
                        _instance.summary = request.POST[i]
                    elif i=='shareholding':
                        _instance.shareholding =request.POST[i]
                    elif i=='roi':
                        _instance.roi =request.POST[i]
                    elif i=='strategy':
                        _instance.strategy =request.POST[i]

                _instance.save()
                _item_object = model_to_dict(InvestmentDetails.objects.get(pk=id))
                data= {}
                data['model']=_item_object		
            
                return JsonResponse({'error': False, 'data': data})
            
            except (KeyError, InvestmentDetails.DoesNotExist):
                #errors = form.errors
                errors= {'__all__': ['No data changed']} 
                return JsonResponse({'erro': True, 'data': errors})
            else:
                return JsonResponse({'error': False, 'data': _item_object})
        else:
            return JsonResponse({'error': True, 'data': "errors encontered"})
    else:
        error = {
            'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json")

@login_required(login_url="account_login")
def add_model_investment_paragraph_ajax(request, id, *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax(): 
            #investment_id = request.POST['investment']			
          
            investment = get_object_or_404(Investment,pk=id)
            record, created=InvestmentDetails.objects.get_or_create(investment=investment)
            for i in request.POST:
                if i=='summary':
                    record.summary=request.POST[i]
                    record.save()
                elif i=='shareholding':
                    record.shareholding=request.POST[i]
                    record.save()
                elif i=='roi':
                    record.roi=request.POST[i]
                    record.save()
                elif i=='strategy':
                    #print(created, record)
                    record.strategy=request.POST[i]
                    record.save()            

            latest = InvestmentDetails.objects.latest('id').id
            _instance = InvestmentDetails.objects.get(pk=latest)
            item_object = model_to_dict(_instance)
            data= {}
            data['model']=item_object		
            
            return JsonResponse({'error': False, 'data': data})
            #item_object['model_id']=investment_id
            #item_object['model_name']=i.usermodel.name
            #print("returned data", item_object)
                
        else:
            return JsonResponse({'error': True, 'data': "errors encontered"})
    else:
        error = {
            'message': 'Error, must be an Ajax call.'
        }
        return JsonResponse(error, content_type="application/json")


def display_business_ajax(request):
    current_time = timezone.now()#datetime.datetime.now()
    if request.method == 'POST':
        bus_status = request.POST.get('bus_status', None)
        if bus_status == None:
            userdata= Investment.objects.filter(creater=request.user) 
        else:  
            if bus_status =="unread":
                userdata = Investment.objects.filter(Q(creater=request.user),Q(investor__application_status='pending') )
            elif bus_status =="closed": 
                userdata = Investment.objects.filter(Q(creater=request.user),Q(closing_date__lt=current_time) )
            elif bus_status =="open":
                userdata = Investment.objects.filter(Q(creater=request.user), Q(closing_date__gte=current_time))
            else:
                userdata = Investment.objects.filter(creater=request.user)

    else:
        userdata= Investment.objects.filter(creater=request.user)

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

            # name 
            # description
            #cdate= i.date_created.ctime()
            item_object = model_to_dict(i)
            item_object['category']=i.category.name
            item_object['closing_date']=i.closing_date.ctime()
            item_object['date_created']=f'{i.date_created.ctime()}'
            item_object['current_investment']=i.current_investment
            item_object['user_stake']=i.userIsInvestorStake(request.user)
            item_object['current_investment_percent']=i.current_investment_percent 
            item_object['blogs_count']=i.blogs_count
            item_object['incoming_investors']=i.incoming_investors 
            item_object['user_investor']=i.userIsInvestorStatement(request.user)
            item_object['userIsOwner']=i.userIsOwner(request.user)
            item_object['user_investment_value']=i.userInvestorValue(request.user)
            item_object['user_investment_percent']=i.userInvestorPercent(request.user)
            item_object['investors_count']=i.investors_count                
            item_object['total_value']=i.total_value
            taglist = []
            for j in i.tags.all():
                   taglist.append(j.name)
            item_object['tags']= taglist
                
            results.append(item_object)
		
        data["results"]=results
        return JsonResponse({"data":data})



def display_myinvestment_ajax(request): 

    queryset = Investor.objects.filter(user=request.user).first()  
    
    if request.method == 'POST':
        app_status = request.POST.get('app_status', None)
        if app_status == None:
            df=queryset.trading_df

        else: 
            if app_status=='all':
                app_status=None
            df=queryset.trading_df_status(app_status)
        #print(app_status)
    else:
        df=queryset.trading_df
    
    if len(df)>0 :
        df['id'] = pd.to_numeric(df.id)
    userdata, _= dataframe_to_list_dict(df,True)
    #print(3, userdata)
    if not ('pertable' in request.session):
        obj= UserPreference.objects.filter(user=request.user).first()
        if obj:
            request.session['pertable']=obj.pertable
        else:# nothing in db
            request.session['pertable']= 3
    pertable=request.session['pertable']
    obj_paginator = Paginator(userdata, pertable)
    if request.method == 'POST':
        app_status = request.POST.get('app_status', None)
        page_no = request.POST.get('page_no', None)
        num_of_pages= int(obj_paginator.num_pages)
        totalrecords= int(obj_paginator.count)
        current_page = obj_paginator.get_page(page_no)   
        data={}	
        data["per_table"]=pertable
        data["page_no"]=page_no
        data["num_of_pages"]=num_of_pages
        #print('num_of_pages:', num_of_pages) 
        data["totalrecords"]=totalrecords
        
      
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
            item_object = {}
            item_object['summary']=i['summary']
            item_object['total_value']=i['total_value']
            item_object['myinvest']=i['myinvest']
            item_object['application_status']=i['application_status']
            item_object['cat_name']=i['cat_name']
            item_object['email']=i['email']
            item_object['inv_name']=i['inv_name']
            item_object['id']=i['id']
            item_object['iid']=i['iid']
            investment_id = i['iid']
            investment_obj= get_object_or_404(Investment, pk=investment_id)
            item_object['blogs_count']=investment_obj.blogs_count  
           
            results.append(item_object)

        #print(results)
        data["results"]=results
        return JsonResponse({"data":data})

@login_required(login_url="account_login")
def update_investorStatus_ajax(request, id, *args, **kwargs):
    investor_obj = get_object_or_404(Investor,pk=id)

    if request.method == 'POST':
        if request.is_ajax():
            form = InvestorStatusUpdateAjax(data=request.POST or None,instance=investor_obj)#, user=request.user)
           
            if form.is_valid():
                investor_obj.date_status_changed= timezone.now()#datetime.datetime.now()
                #correct here also
                investor_obj.save()
                form.save()
                
               
            else:
                errors = form.errors
                #print('error:' , errors)
                return JsonResponse({'error': True, 'data': errors})  
            
            latest = Investor.objects.latest('id').id
            record = Investor.objects.get(pk=latest)
            item_object = model_to_dict(record)
            queryset = Investor.objects.filter(Q(user=request.user),Q(application_status='accepted'))#    
           
            #print (item_object)
            return JsonResponse({'error': False, 'data': item_object,'accepted': queryset.count() })
        else:
            return JsonResponse({'error': True, 'data': "Request not ajax"})
  
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})


def download_investor_list(request, pk):
   return get_excel_investor_list(request, pk)


@admin_only
def dbUpdateInvestorsRecieved(request):
    updateInvestorApplicationState(request)
    return HttpResponseRedirect(reverse('trading_home', args=())) 


# Display a specific invoice
@login_required(login_url="account_login")
def investment_dashboard(request, pk):
    project = get_object_or_404(Investment, pk=pk, creater=request.user)
    engaged=project.engaged_investment
    #wip=project.engaged_investment
    project_target =project.total_value
    outstanding= max(project_target - engaged,0)
    #use interpolation, momentum, AI. ML
    
    context = {        
        'project' : project,
        #'wip':wip,
        'engaged':engaged,
        'perfomance':engaged *100/project_target if project_target !=0 else 0,
        'outstanding':outstanding,
        #'month_expected_output':month_expected_output
        
    }
    #-----project model require an id-----------
    dummy_project= model_to_dict(project)
   
    dummy_project['due_date']= None# date cannot be serialised
    dummy_project['value']= None # decimal cannot be serialised
    request.session['project_id']= project.id#dummy_project
    #---------------------------

     
    #--last month
    first_day_this_month = date.today().replace(day=1)
    last_day_of_this_month = last_day_of_month(first_day_this_month)
    
    previous_last = first_day_this_month - timedelta(days=1)
    previous_first = previous_last.replace(day=1)
    context['last_month'] = previous_first

    date_first_output = project.date_first_output
    #print(date_first_output)
    context['today'] = date.today()        
    context['minus_3_months'] = date.today() - relativedelta(months=3)
    context['minus_6_months'] = date.today() - relativedelta(months=6)
    context['minus_12_months'] = date.today() - relativedelta(years=1) 
    context['minus_full_period'] = date_first_output      
    start_of_week=date.today() - timedelta(days=date.today().weekday())
    context['first_day_of_week'] =start_of_week
    context['last_day_of_week'] =start_of_week + timedelta(days=6)
    context['first_day_of_month'] = date.today().replace(day=1)
    context['last_day_of_month'] = last_day_of_month(date.today())
    #---locomotives
    get_project_outputs_monthly(request, first_day_this_month, last_day_of_this_month, context)
    #import json
    
   
    if isinstance(date_first_output,datetime.datetime):
        dt = date_first_output.replace(tzinfo=None)
        context['minus_full_period'] =dt.date()#json.dumps(dt.date(), default=str)
    else:
        context['minus_full_period'] =date_first_output
    #context['minus_full_period'] = date_first_output.isoformat()#json_serial(date_first_output)
    
    #use better prediction method
    if 'previous_releases' in context and 'releases' in context:
        context['month_expected_output']=(context['previous_releases']+ context['releases'])/2 #project.expected_output_curr_month
    else:
        context['month_expected_output']=0
    options_list = get_userprefs_graph_options(request)#[1,3]
    options_json = json.dumps(options_list)
    context['json_userprefs_graph_options'] =options_json
    
    return render(request, 'trading/investment_dashboard.html', context)

def get_userprefs_graph_options(request):
    pref, created = ProjectOuputGraphPreference.objects.get_or_create(user=request.user)
    options_list=[]
    list_ =[pref.g1,pref.g2,pref.g3,pref.g4,pref.g5,pref.g6]
    #print('object attributes >>>>>>', dir(pref))
    #print('__dict__...', pref.__dict__.keys())
    fields= pref.__dict__.keys()
    restricted_fields= ['_state', 'id', 'user_id', 'last_modified']
    #list_2 =[pref.x for x in fields]
    #print(list_2)
    
    for i in range(len(list_)):
        if list_[i]==True:
            options_list.append(i+1)
    return options_list
class ProjectOuputGraphPreferenceCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = ProjectOuputGraphPreference
    
    template_name = 'trading/project_output_pref.html'
    success_url = reverse_lazy('trading_home')
    form_class = ProjectOuputGraphPreferenceForm
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

    def get_form_class(self):
        return ProjectOuputGraphPreferenceForm

    def get_context_data(self, **kwargs):
        context = super(ProjectOuputGraphPreferenceCreate, self).get_context_data(**kwargs)
        context['menu'] = 'prefer'
        context['submenu'] = "prefer" #self.type
        context['project_id'] = self.request.session['project_id']
        return context
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def update_project_graph_pref(request):
    pref, created = ProjectOuputGraphPreference.objects.get_or_create(user=request.user)
    #print(pref)
    if request.method == 'POST':
        form = ProjectOuputGraphPreferenceForm(request.POST or None,instance=pref)
        form.instance.user =request.user
        if form.is_valid():
            form.save()
            project_id = request.session['project_id']
            #print(type(project_id),project_id)
            id=str(project_id)
            return HttpResponseRedirect(reverse('investment_dashboard',args=(id,))) 
    else:
        form = ProjectOuputGraphPreferenceForm(instance=pref)
        context ={}
        context['form']=form
        context['project_id'] = request.session['project_id']
        return render(request, 'trading/project_output_pref.html', context)

#defunct also
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))