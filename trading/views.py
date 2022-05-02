
from django.shortcuts import get_object_or_404, render
from common.decorators import admin_only

from investments_appraisal.models import ModelCategory, UserModel, UserPreference
from django.http import JsonResponse
from django.core.paginator import Paginator

from trading.forms import InvestmentROIForm, InvestmentShareholdingForm, InvestmentStrategyForm, InvestmentSummaryForm, InvestorForm, InvestorFormUpdate, UserInvestmentForm, UserInvestmentFormUpdate
from .models import *
from django.db.models.expressions import F
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group

from django.template.loader import render_to_string

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="account_login")
def get_user_businesses(request):
    queryset = Investment.objects.filter(creater=request.user)
    form = UserInvestmentForm(initial={'creater': request.user})
    context = {
        "models": queryset,
        "total": queryset.count(),
        "user": request.user,
        'form': form,
    }

    return render(request, 'trading/user_businesses.html', context)


    

@login_required(login_url="account_login")
def get_user_investments(request):
    queryset = Investor.objects.filter(user=request.user).first()  
    df=queryset.trading_df
    #df['id']= df['id'].astype()
    df['id'] = pd.to_numeric(df.id)
    # print(df.columns)
    # inv_name', 'summary', 'total_value', 'username', 'first_name',
    # 'last_name', 'email', 'cat_name', 'cat_descript', 'uniqueid'
    # max_val = df['value'].max()
    # min_val = df['value'].min()
    sum_total = df['myinvest'].sum()
    aver_val = df['myinvest'].mean()
    # print(df)
    dict_,colms= dataframe_to_list_dict(df,True)
    # print(dict_)
    # print(colms)
    
    context = {
        "models": dict_,
        "total": len(dict_),
        'total_sum':sum_total,
        'average':aver_val
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
		return JsonResponse({'error': False, 'data': item_object})
	else:
		return JsonResponse({'error': True, 'data': "Request not ajax"})

def investment_search_ajax(request,slug, *args, **kwargs):
    #
    if request.method == 'POST':
        #description= request.POST['description']
        modelsdata= Investment.objects.filter(description__icontains=slug)

        if not ('perpage' in request.session):
            if request.user.is_authenticated:
                obj= UserPreference.objects.filter(user=request.user).first()
                # anonymous user is not iterable
                if obj:
                    request.session['perpage']=obj.perpage
                else:# nothing in db
                    request.session['perpage']= 3
            else:
                request.session['perpage']= 3

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
                item_object['date_created']=f'new Date("{i.date_created.ctime()}")'
                item_object['date_created']=f'{i.date_created.ctime()}'
                item_object['uniqueid']=i.category.uniqueid
                item_object['userIsInvestor']=i.userIsInvestor(request.user)
                results.append(item_object)
                
            data["results"]=results
        
        return JsonResponse({"data":data})


def display_investment_ajax(request):
    models= Investment.objects.all()#.order_by('-date')


    per_page=3
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
            item_object['date_created']=f'new Date("{i.date_created.ctime()}")'
            item_object['date_created']=f'{i.date_created.ctime()}'
            item_object['uniqueid']=i.category.uniqueid
            item_object['userIsInvestor']=i.userIsInvestor(request.user)
            #print(item_object)
            results.append(item_object)
        
        data["results"]=results
        
        
        return JsonResponse({"data":data})


        
@login_required
def investment_details(request,id):
    investmet_obj = get_object_or_404(Investment,pk=id)
    id =investmet_obj.id
    is_user_investor=False
    investor_id=1
    obj=Investor.objects.filter(user=request.user, investment=id) 
    if obj:
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
def home(request):
	models= Investment.objects.all()
	
	per_page=3
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
                    item_object['investors_count']=parent_invest.investors_count
                item_object['investor_id']=pk
                
                
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
            item_object['investors_count']= record.investors_count
            item_object['date_created']= record.date_created.ctime()
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
                item_object['investors_count']=parent_invest.investors_count
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
def delete_investor_ajax(request, id, *args, **kwargs):
	if request.method == 'POST':
		#print(request.POST)
		if request.is_ajax():
			
			model_ = get_object_or_404(Investor, pk=id)

			model_.delete()
			item_object = model_to_dict(model_)

			#total_pages= get_total_pages(request)
			data= {}
			#data['total_pages']=total_pages
			#data['deleted_page']=page_no
			
			data['model']=item_object
			
			#messages.success(request, "Successfully deleted  model")
			
			return JsonResponse({'error': False, 'data': data})
			
		else:
			return JsonResponse({'error': True, 'data': "errors encontered"})
	else:
		error = {
			'message': 'Error, must be an Ajax call.'
		}
		return JsonResponse(error, content_type="application/json")

@login_required(login_url="account_login")
def delete_investment_ajax(request, id, *args, **kwargs):
	if request.method == 'POST':
		#print(request.POST)
		if request.is_ajax():
			
			model_ = get_object_or_404(Investment, pk=id)

			model_.delete()
			prices_item_object = model_to_dict(model_)

			#total_pages= get_total_pages(request)
			data= {}
			#data['total_pages']=total_pages
			#data['deleted_page']=page_no
			
			data['model']=prices_item_object
			
			#messages.success(request, "Successfully deleted  model")
			
			return JsonResponse({'error': False, 'data': data})
			
		else:
			return JsonResponse({'error': True, 'data': "errors encontered"})
	else:
		error = {
			'message': 'Error, must be an Ajax call.'
		}
		return JsonResponse(error, content_type="application/json")

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
        item_instance = get_object_or_404(Investment,pk=pk)
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
            print(item_object)
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
        print(request.POST)
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
           
            for i in request.POST:
                if i=='summary':
                    record = InvestmentDetails.objects.create(investment=investment, summary=request.POST[i])
                    record.save()
                elif i=='shareholding':
                    record = InvestmentDetails.objects.create(investment=investment, shareholding=request.POST[i])
                    record.save()
                elif i=='roi':
                    record = InvestmentDetails.objects.create(investment=investment, roi=request.POST[i])
                    record.save()
                elif i=='strategy':
                    record = InvestmentDetails.objects.create(investment=investment, strategy=request.POST[i])
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
