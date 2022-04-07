from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
import datetime

from django.db.models import Q
from beefapp.forms import FeedlotDesignParametersForm
from beefapp.models import FeedlotDesignParameters
from fishapp.forms import TankDesignParametersForm
from fishapp.models import TankDesignParameters

from common.decorators import unauthenticated_user, allowed_users, admin_only, \
     registered_user_only_with_client_routing


from django.template.loader import render_to_string

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.conf import settings
from common.models import ModifiedRecord
from django.views.decorators.csrf import csrf_exempt




from django.shortcuts import render
from plotly.offline import download_plotlyjs, plot
import plotly.offline as opy
import plotly.graph_objs as go
import chart_studio.plotly as py
import os
import numpy as np
from datetime import datetime
from plotly.graph_objs import Scatter
import plotly.express as px
import pandas as pd


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import datetime
from datetime import date
import os
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.forms.models import model_to_dict
import decimal
import csv
from itertools import chain

from tempfile import NamedTemporaryFile


import pandas as pd
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils.decorators import method_decorator


import functools

from django.conf import settings
from django.views.generic import DetailView


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group



from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic


from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from investments_appraisal.models import *

from investments_appraisal.forms import  FinancingForm, MacroeconomicParametersForm, TimingAssumptionForm, \
	  PricesForm,DepreciationForm ,TaxesForm,  WorkingCapitalForm

@login_required(login_url="account_login")
def add_model_specs_page_mentor(request, model_id):

	usermodel = get_object_or_404(UserModel,pk=model_id)
	simulation_iterations=usermodel.simulation_iterations 
	interva_l =min(max(simulation_iterations/10,50000),150000)
	user_modeltype=	usermodel.model_type.uniqueid

	progress_count=0
	#1. Model Timing Assumptions
	model_ta = TimingAssumption.objects.filter(usermodel=usermodel).first()
	if model_ta :
		#increment
		progress_count +=1		
		timing_assumptions_form = TimingAssumptionForm(instance=model_ta)
	else:
		timing_assumptions_form = TimingAssumptionForm(initial={'usermodel': usermodel})
    
	#2. Model Prices
	model_prices = Prices.objects.filter(usermodel=usermodel).first()
	if model_prices :
		#increment
		progress_count +=1		
		prices_form = PricesForm(instance=model_prices)
	else:
		prices_form = PricesForm(initial={'usermodel': usermodel})

	#3. Model Depreciation
	model_depreciation = Depreciation.objects.filter(usermodel=usermodel).first()
	if model_depreciation :
		#increment
		progress_count +=1		
		depreciation_form = DepreciationForm(instance=model_depreciation)
	else:
		depreciation_form = DepreciationForm(initial={'usermodel': usermodel})	

    #4. Model Taxes
	model_taxes = Taxes.objects.filter(usermodel=usermodel).first()
	if model_taxes :
		#increment
		progress_count +=1		
		taxes_form = TaxesForm(instance=model_taxes)
	else:
		taxes_form = TaxesForm(initial={'usermodel': usermodel})	
    
	#5. Model Financing
	model_financing = Financing.objects.filter(usermodel=usermodel).first()
	if model_financing :
		#increment
		progress_count +=1		
		financing_form = FinancingForm(instance=model_financing)
	else:
		financing_form = FinancingForm(initial={'usermodel': usermodel})

    #6. Model WorkingCapital
	model_workingcapital = WorkingCapital.objects.filter(usermodel=usermodel).first()
	if model_workingcapital :
		#increment
		progress_count +=1		
		workingcapital_form = WorkingCapitalForm(instance=model_workingcapital)
	else:
		workingcapital_form = WorkingCapitalForm(initial={'usermodel': usermodel})

	#7. Model MacroeconomicParameters
	model_macroeconomicparameters = MacroeconomicParameters.objects.filter(usermodel=usermodel).first()
	if model_macroeconomicparameters :
		#increment
		progress_count +=1		
		macroeconomicparameters_form = MacroeconomicParametersForm(instance=model_macroeconomicparameters)
	else:
		macroeconomicparameters_form = MacroeconomicParametersForm(initial={'usermodel': usermodel})
		
    # #8. Model FeedlotDesignParametersForm
	# model_feedlotdesignparameters = FeedlotDesignParameters.objects.filter(usermodel=usermodel).first()
	# if model_feedlotdesignparameters :

	# 	feedlotdesignparameters_form = FeedlotDesignParametersForm(instance=model_feedlotdesignparameters)
	# else:
	# 	feedlotdesignparameters_form = FeedlotDesignParametersForm(initial={'usermodel': usermodel})
	
    #9. Model TankDesignParameterForm
	model_tankdesignparameters = TankDesignParameters.objects.filter(usermodel=usermodel).first()
	if model_tankdesignparameters :	
		#increment
		progress_count +=1	
		tankdesignparameters_form = TankDesignParametersForm(instance=model_tankdesignparameters)
	else:
		tankdesignparameters_form = TankDesignParametersForm(initial={'usermodel': usermodel})

	
	#-----------title name------------------
	date_now = datetime.datetime.now() #date.today()
	date_now = str(date_now.year) + '_' + str(date_now.month) \
				+ '_' + str(date_now.day)+ "_" + str(date_now.hour) \
				+ '_' + str(date_now.minute) + "_" +  str(date_now.second)
	user_doc_name = f"clearVision_solutions_{user_modeltype}_" + str(date_now)
	#-----------------------------

	context = {
			"user": request.user,
			"employees_page": "active",
			"price_record": model_prices,
			"usermodel": usermodel,
			"timing_assumptions_form": timing_assumptions_form,
			"ta_record": model_ta,
			"prices_form": prices_form,
			'depreciation_record': model_depreciation,
			"depreciation_form": depreciation_form,
			'taxes_record': model_taxes,
			"taxes_form": taxes_form,
			'financing_record': model_financing,
			"financing_form": financing_form,
			'workingcapital_record': model_workingcapital,
			"workingcapital_form": workingcapital_form,
			'macroeconomicparameters_record': model_macroeconomicparameters,
			"macroeconomicparameters_form": macroeconomicparameters_form,
			"tankdesignparameters_form": tankdesignparameters_form,			
			'interva_l':interva_l,
			'user_doc_name':user_doc_name,
			'tankdesignparameters_record': model_tankdesignparameters,
			'progress_count':progress_count,

		}  
	
   
	return render(request, 'fishapp/mentor/model-details.html', context)

@login_required(login_url="account_login")
def add_model_specs_page(request, model_id):

	usermodel = get_object_or_404(UserModel,pk=model_id)
	simulation_iterations=usermodel.simulation_iterations 
	interva_l =min(max(simulation_iterations/10,50000),150000)
	user_modeltype=	usermodel.model_type.uniqueid

	progress_count=0
	#1. Model Timing Assumptions
	model_ta = TimingAssumption.objects.filter(usermodel=usermodel).first()
	if model_ta :
		#increment
		progress_count +=1		
		timing_assumptions_form = TimingAssumptionForm(instance=model_ta)
	else:
		timing_assumptions_form = TimingAssumptionForm(initial={'usermodel': usermodel})
    
	#2. Model Prices
	model_prices = Prices.objects.filter(usermodel=usermodel).first()
	if model_prices :
		#increment
		progress_count +=1		
		prices_form = PricesForm(instance=model_prices)
	else:
		prices_form = PricesForm(initial={'usermodel': usermodel})

	#3. Model Depreciation
	model_depreciation = Depreciation.objects.filter(usermodel=usermodel).first()
	if model_depreciation :
		#increment
		progress_count +=1		
		depreciation_form = DepreciationForm(instance=model_depreciation)
	else:
		depreciation_form = DepreciationForm(initial={'usermodel': usermodel})	

    #4. Model Taxes
	model_taxes = Taxes.objects.filter(usermodel=usermodel).first()
	if model_taxes :
		#increment
		progress_count +=1		
		taxes_form = TaxesForm(instance=model_taxes)
	else:
		taxes_form = TaxesForm(initial={'usermodel': usermodel})	
    
	#5. Model Financing
	model_financing = Financing.objects.filter(usermodel=usermodel).first()
	if model_financing :
		#increment
		progress_count +=1		
		financing_form = FinancingForm(instance=model_financing)
	else:
		financing_form = FinancingForm(initial={'usermodel': usermodel})

    #6. Model WorkingCapital
	model_workingcapital = WorkingCapital.objects.filter(usermodel=usermodel).first()
	if model_workingcapital :
		#increment
		progress_count +=1		
		workingcapital_form = WorkingCapitalForm(instance=model_workingcapital)
	else:
		workingcapital_form = WorkingCapitalForm(initial={'usermodel': usermodel})

	#7. Model MacroeconomicParameters
	model_macroeconomicparameters = MacroeconomicParameters.objects.filter(usermodel=usermodel).first()
	if model_macroeconomicparameters :
		#increment
		progress_count +=1		
		macroeconomicparameters_form = MacroeconomicParametersForm(instance=model_macroeconomicparameters)
	else:
		macroeconomicparameters_form = MacroeconomicParametersForm(initial={'usermodel': usermodel})
		
    # #8. Model FeedlotDesignParametersForm
	# model_feedlotdesignparameters = FeedlotDesignParameters.objects.filter(usermodel=usermodel).first()
	# if model_feedlotdesignparameters :

	# 	feedlotdesignparameters_form = FeedlotDesignParametersForm(instance=model_feedlotdesignparameters)
	# else:
	# 	feedlotdesignparameters_form = FeedlotDesignParametersForm(initial={'usermodel': usermodel})
	
    #9. Model TankDesignParameterForm
	model_tankdesignparameters = TankDesignParameters.objects.filter(usermodel=usermodel).first()
	if model_tankdesignparameters :	
		#increment
		progress_count +=1	
		tankdesignparameters_form = TankDesignParametersForm(instance=model_tankdesignparameters)
	else:
		tankdesignparameters_form = TankDesignParametersForm(initial={'usermodel': usermodel})

	
	#-----------title name------------------
	date_now = datetime.datetime.now() #date.today()
	date_now = str(date_now.year) + '_' + str(date_now.month) \
				+ '_' + str(date_now.day)+ "_" + str(date_now.hour) \
				+ '_' + str(date_now.minute) + "_" +  str(date_now.second)
	user_doc_name = f"clearVision_solutions_{user_modeltype}_" + str(date_now)
	#-----------------------------

	context = {
			"user": request.user,
			"employees_page": "active",
			"price_record": model_prices,
			"usermodel": usermodel,
			"timing_assumptions_form": timing_assumptions_form,
			"ta_record": model_ta,
			"prices_form": prices_form,
			'depreciation_record': model_depreciation,
			"depreciation_form": depreciation_form,
			'taxes_record': model_taxes,
			"taxes_form": taxes_form,
			'financing_record': model_financing,
			"financing_form": financing_form,
			'workingcapital_record': model_workingcapital,
			"workingcapital_form": workingcapital_form,
			'macroeconomicparameters_record': model_macroeconomicparameters,
			"macroeconomicparameters_form": macroeconomicparameters_form,
            # 'feedlotdesignparameters_record': model_feedlotdesignparameters,
			# "feedlotdesignparameters_form": feedlotdesignparameters_form,
			"tankdesignparameters_form": tankdesignparameters_form,			
			'interva_l':interva_l,
			'user_doc_name':user_doc_name,
			'tankdesignparameters_record': model_tankdesignparameters,
			'progress_count':progress_count,

		}  
	

	return render(request, 'fishapp/user_model_specs.html', context)

@login_required(login_url="account_login")
def add_model_tankdesignparameters_ajax(request,  *args, **kwargs):
	if request.method == 'POST':
		if request.is_ajax(): 

			usermodel_id = request.POST['usermodel']
			
			
			tank_length = request.POST['tank_length']
			tank_width = request.POST['tank_width']
			depth = request.POST['depth']

			volume_of_water = request.POST['volume_of_water']
			density_per_cubic_metre = request.POST['density_per_cubic_metre']
			total_fish_per_tank_per_cycle = request.POST['total_fish_per_tank_per_cycle']
			tank_num_of_months_per_cycle = request.POST['tank_num_of_months_per_cycle']
			fish_per_tank_per_year = request.POST['fish_per_tank_per_year']
			num_of_tanks = request.POST['num_of_tanks']

		
			
			
			tank_length= decimal.Decimal(tank_length) if tank_length else 0.0
			tank_width= decimal.Decimal(tank_width) if tank_width else 0.0
			depth= decimal.Decimal(depth) if depth else 0.0
			volume_of_water= decimal.Decimal(volume_of_water) if volume_of_water else 0.0
			density_per_cubic_metre= decimal.Decimal(density_per_cubic_metre) if density_per_cubic_metre else 0.0

			
			usermodel = get_object_or_404(UserModel,pk=usermodel_id)
		
		
			i = TankDesignParameters.objects.create(usermodel=usermodel, tank_length=tank_length,
					tank_width=tank_width, depth=depth,volume_of_water=volume_of_water, 
					density_per_cubic_metre=density_per_cubic_metre,
					total_fish_per_tank_per_cycle=total_fish_per_tank_per_cycle,
					tank_num_of_months_per_cycle=tank_num_of_months_per_cycle,
					num_of_tanks=num_of_tanks,
					fish_per_tank_per_year=fish_per_tank_per_year)
			i.save()
			

			latest = TankDesignParameters.objects.latest('id').id
			_instance = TankDesignParameters.objects.get(pk=latest)
			item_object = model_to_dict(_instance)
			item_object['model_id']=usermodel_id
			item_object['model_name']=i.usermodel.name
			#print("returned data", item_object)
				
			messages.success(request, "Successfully added TankDesign parameters")
			
			return JsonResponse({'error': False, 'data': item_object})
				
		else:
			return JsonResponse({'error': True, 'data': "errors encontered"})
	else:
		error = {
			'message': 'Error, must be an Ajax call.'
		}
		return JsonResponse(error, content_type="application/json")


#Tank Design Parameters--------------------------------------------------
@login_required(login_url="account_login")
def edit_model_tankdesignparameters_ajax(request, id, *args, **kwargs):
	if request.method == 'POST':
		if request.is_ajax():

			tank_length = request.POST['tank_length']
			tank_width = request.POST['tank_width']
			depth = request.POST['depth']

			volume_of_water = request.POST['volume_of_water']
			density_per_cubic_metre = request.POST['density_per_cubic_metre']
			total_fish_per_tank_per_cycle = request.POST['total_fish_per_tank_per_cycle']
			tank_num_of_months_per_cycle = request.POST['tank_num_of_months_per_cycle']
			fish_per_tank_per_year = request.POST['fish_per_tank_per_year']
			num_of_tanks = request.POST['num_of_tanks']

			
			
			tank_length= decimal.Decimal(tank_length) if tank_length else 0.0
			tank_width= decimal.Decimal(tank_width) if tank_width else 0.0
			depth= decimal.Decimal(depth) if depth else 0.0
			volume_of_water= decimal.Decimal(volume_of_water) if volume_of_water else 0.0
			density_per_cubic_metre= decimal.Decimal(density_per_cubic_metre) if density_per_cubic_metre else 0.0

		
		
			_instance = get_object_or_404(TankDesignParameters, pk=id)
			
		
			try:
				_instance.tank_length =tank_length
				_instance.tank_width =tank_width
				_instance.depth =depth
				_instance.fish_per_tank_per_year =fish_per_tank_per_year

				_instance.density_per_cubic_metre =density_per_cubic_metre
				_instance.volume_of_water =volume_of_water
				_instance.total_fish_per_tank_per_cycle =total_fish_per_tank_per_cycle
				_instance.tank_num_of_months_per_cycle =tank_num_of_months_per_cycle
				_instance.total_fish_per_tank_per_cycle =total_fish_per_tank_per_cycle
				_instance.num_of_tanks =num_of_tanks

				_instance.save()

				_item_object = model_to_dict(TankDesignParameters.objects.get(pk=id))
				
				return JsonResponse({'error': False, 'data': _item_object})
			
			except (KeyError, TankDesignParameters.DoesNotExist):
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


 
#Check is requirement met--------------------------------------------------
@login_required(login_url="account_login")
def check_run_requirements_ajax(request, model_id, *args, **kwargs):
	if request.method == 'POST':
		if request.is_ajax():

			usermodel = get_object_or_404(UserModel,pk=model_id)
			progress_count=0
			#1. Model Timing Assumptions
			model_ta = TimingAssumption.objects.filter(usermodel=usermodel).first()
			if model_ta :
				progress_count+=1	
			
			#2. Model Prices
			model_prices = Prices.objects.filter(usermodel=usermodel).first()
			if model_prices :	
				progress_count+=1

			#3. Model Depreciation
			model_depreciation = Depreciation.objects.filter(usermodel=usermodel).first()
			if model_depreciation :	
				progress_count+=1
			#4. Model Taxes
			model_taxes = Taxes.objects.filter(usermodel=usermodel).first()
			if model_taxes :	
				progress_count+=1
			#5. Model Financing
			model_financing = Financing.objects.filter(usermodel=usermodel).first()
			if model_financing :	
				progress_count+=1
			#6. Model WorkingCapital
			model_workingcapital = WorkingCapital.objects.filter(usermodel=usermodel).first()
			if model_workingcapital :	
				progress_count+=1
			#7. Model MacroeconomicParameters
			model_macroeconomicparameters = MacroeconomicParameters.objects.filter(usermodel=usermodel).first()
			if model_macroeconomicparameters :	
				progress_count+=1
			
			#9. Model TankDesignParameterForm
			model_tankdesignparameters = TankDesignParameters.objects.filter(usermodel=usermodel).first()
			if model_tankdesignparameters :	
				progress_count+=1
			
		   
			#succes here
			if progress_count<8:
				return JsonResponse({'error': False, 'data': False, 'status': f'{progress_count} of 8 Complete'})
			else:
				#update database
				usermodel.design_complete= True
				usermodel.save()
				return JsonResponse({'error': False, 'data': True, 'status': f'{progress_count} of 8 Complete'})
			
		
		else:
			return JsonResponse({'error': True, 'data': "errors encontered"})
	else:
		error = {
			'message': 'Error, must be an Ajax call.'
		}
		return JsonResponse(error, content_type="application/json")
