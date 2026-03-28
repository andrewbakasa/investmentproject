 
 
# Create your views here.
import copy
import math

import numpy as np
import pandas as pd
from common.data_utils import create_downloads_instance, create_user_model_downloads_instance
from common.utils import get_current_user_groups
from fishapp.fish_bus_model import FishBusinessReport
from fishapp.models import TankDesignParameters
#old class
#from investments_appraisal.bus_models import BeefBusinessReport
#switch here

from investments_appraisal.models import *
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from beefapp.model_constants_beef import *
from fishapp.model_constants_fish import *
from investments_appraisal.whatif import data_table, get_data_table_sensitivity_in_parrallel, get_sensitivity_gradient, monteCarlo_sim, parallel_data_table 
#from scipy import stats
from tqdm import tqdm
# Default invoice list, show 25 recent invoices
from django.http import JsonResponse




@login_required(login_url="account_login")
def get_model_spreadsheets(request, model_id):
    request.session['count']=0
    #to correct errorer
    request.session['total_runs'] =100000
    request.session.save()
    usermodel = get_object_or_404(UserModel,pk=model_id)
    simulation_iterations=usermodel.simulation_iterations
    total_params=usermodel.total_params 
    simulation_run=usermodel.simulation_run 
    npv_bin_size=usermodel.npv_bin_size
    
    #change to description
    user_model_decription =usermodel.description

    run_check_counter=0
    #1. Model Timing Assumptions        
    model_ta = TimingAssumption.objects.filter(usermodel=usermodel).first()
    if model_ta:
        # TIMING ASSUMPTIONS
        #increment checking
        run_check_counter+=1
        timing_assumptions = {
            'base_period': {'title': 'Base Period','value': model_ta.base_period}, 
            'construction_start_year': {'title': 'Construction start Year','value': model_ta.construction_start_year},
            'construction_len': {'title': 'Construction length','value': model_ta.construction_len}, 
            'construction_year_end': {'title': 'Construction End Year','value': model_ta.construction_year_end},#one year
            'operation_start_year': {'title': 'Operation Start Year','value': model_ta.operation_start_year}, 
            'operation_duration': {'title': 'Operation Duration','value': model_ta.operation_duration},
            'operation_end': {'title': 'Operation End ','value': model_ta.operation_end}, 
            'number_of_months_in_a_year': {'title': 'Number of months in a year','value': model_ta.number_of_months_in_a_year},
            }

    model_prices = Prices.objects.filter(usermodel=usermodel).first()
    if model_prices:
        #increment checking
        run_check_counter+=1
        # PRICES
        prices = {
            'title': 'Net Sales Price:', #model_prices.title
            'base_price': float(model_prices.base_price), 
            'change_in_price': float(model_prices.change_in_price), 
        }

    model_depreciation = Depreciation.objects.filter(usermodel=usermodel).first()
    if model_depreciation:
        #increment checking
        run_check_counter+=1
        # depreciation
        depreciation = {
        'economic_life_of_machinery': {'title': 'Economic life of machinery','value': model_depreciation.economic_life_of_machinery, 'units': 'YEARS'}, 
        'economic_life_of_buildings': {'title': 'Economic life of buildings','value': model_depreciation.economic_life_of_buildings, 'units': 'YEARS'},
        'tax_life_of_machinery': {'title': 'Tax life of machinery','value': model_depreciation.tax_life_of_machinery, 'units': 'YEARS'}, 
        'tax_life_of_buildings': {'title': 'Tax life of buildings','value': model_depreciation.tax_life_of_buildings, 'units': 'YEARS'},
        'tax_life_of_soft_capital_costs': {'title': 'Tax life of soft capital costs','value': model_depreciation.tax_life_of_soft_capital_costs, 'units': 'YEARS'},
    }
    # TAXES--------------
    model_taxes = Taxes.objects.filter(usermodel=usermodel).first()
    if model_taxes:
        #increment checking
        run_check_counter+=1
        # taxes
        taxes = {
            'import_duty': {'title': 'Import duty','value': float(model_taxes.import_duty), 'units': 'PERCENT'}, 
            'sales_tax': {'title': 'Sales tax','value': float(model_taxes.sales_tax), 'units': 'PERCENT'}, 
            'corporate_income_tax': {'title': 'Corporate income tax','value': float(model_taxes.corporate_income_tax), 'units': 'PERCENT'}
        }
    
    # FINANCING--------------
    model_financing = Financing.objects.filter(usermodel=usermodel).first()
    para_senior_debt=0# initialise this
    if model_financing:
        #increment checking
        run_check_counter+=1
       
        financing = {
            'real_interest_rate': {'title': 'Real interest rate','value': float(model_financing.real_interest_rate), 'units': 'PERCENT'}, 
            'risk_premium': {'title': 'Risk premium','value': float(model_financing.risk_premium), 'units': 'PERCENT'}, 
            'num_of_installments': {'title': 'No. of installments','value': int(model_financing.num_of_installments), 'units': 'NUMBER'},  
            'grace_period': {'title': 'Grace period (years)','value':int(model_financing.grace_period), 'units': 'YEARS'}, 
            'repayment_starts': {'title': 'Repayment starts year','value':0, 'units': 'YEAR'}, #recalculated
            'equity': {'title': 'Equity (% of Investment Costs)','value': float(model_financing.equity), 'units': 'PERCENT'}, 
            'senior_debt': {'title': 'Senior Debt (% of Investment Costs)','value': float(model_financing.senior_debt), 'units': 'PERCENT'},  
        }
        para_senior_debt= float(model_financing.senior_debt)
        #sync senior_debt with simulation and investment_option here
        #very important execericxe 03/03/2022 1747hrs

    # Working Capital--------------
    model_workingcapital = WorkingCapital.objects.filter(usermodel=usermodel).first()
    if model_workingcapital:
        #increment checking
        run_check_counter+=1
       
        working_capital = {
            'accounts_receivable': {'title': 'Accounts receivable [% of Gross Sales]','value':float(model_workingcapital.accounts_receivable), 'units': 'PERCENT'}, 
            'accounts_payable': {'title': 'Acccounts payable (% of total input cost)','value': float(model_workingcapital.accounts_payable), 'units': 'PERCENT'}, 
            'cash_balance': {'title': 'Cash balance  (% of gross sales)','value': float(model_workingcapital.cash_balance), 'units': 'PERCENT'},              
        }  
    
    # Macroeconomic Parameters --------------
    model_macroeconomic_parameters = MacroeconomicParameters.objects.filter(usermodel=usermodel).first()
    if model_macroeconomic_parameters:
        #increment checking
        run_check_counter+=1
       
        macroeconomic_parameters = {
        'discount_rate_equity': {'title': 'Discount Rate Equity','value': float(model_macroeconomic_parameters.discount_rate_equity), 'units': 'PERCENT'}, 
        'domestic_inflation_rate': {'title': 'Domestic Inflation rate','value': float(model_macroeconomic_parameters.domestic_inflation_rate), 'units': 'PERCENT'},
        'us_inflation_rate': {'title': 'US Inflation rate','value':float(model_macroeconomic_parameters.us_inflation_rate), 'units': 'PERCENT'}, 
        'exchange_rate': {'title': 'Exchange Rate (LC/USD - in Base Year )','value': float(model_macroeconomic_parameters.exchange_rate), 'units': 'NUMBER'},
        'dividend_payout_ratio': {'title': 'Divident Payout Ratio','value': float(model_macroeconomic_parameters.dividend_payout_ratio), 'units': 'PERCENT'},
        'num_of_shares': {'title': 'N# of shares','value': float(model_macroeconomic_parameters.num_of_shares), 'units': 'NUMBER'},
    }
    #user specs
    investment_cost_fish['investment_costs_over_run_factor']['value']=float(model_macroeconomic_parameters.investment_costs_over_run_factor)
    
    # TankrDesignParameters--------------
    model_tank_design_parameters = TankDesignParameters.objects.filter(usermodel=usermodel).first()
    if model_tank_design_parameters:
        #increment checking
        run_check_counter+=1
        tank_design_parameters = {
            'num_of_tanks': {'title': 'N# Of Tanks','value': float(model_tank_design_parameters.num_of_tanks), 'units': 'NUMBER'}, 
            'length': {'title': 'Length in meters','value': float(model_tank_design_parameters.tank_length), 'units': 'NUMBER'}, 
            'width': {'title': 'Width in meters','value': float(model_tank_design_parameters.tank_width), 'units': 'NUMBER'},
            'depth': {'title': 'Depth in meters','value': float(model_tank_design_parameters.depth), 'units': 'NUMBER'},
            'sqm': {'title': 'SQM covered by Tanks','value': float(model_tank_design_parameters.sqm), 'units': 'NUMBER'},  #Derived  
            'volume_of_water': {'title': 'Volume Of Water/tank','value': float(model_tank_design_parameters.volume_of_water), 'units': 'LITRES'}, 
            'density_per_cubic_metre': {'title': 'Fish Density/[cm]','value':None, 'units': 'NUMBER'},#calculated 
            'total_fish_per_tank_per_cycle': {'title': 'Total Fish in one tank per cycle','value': float(model_tank_design_parameters.total_fish_per_tank_per_cycle), 'units': 'NUMBER'}, 
            'num_of_months_per_cycle': {'title': 'N# of months per cycle','value': float(model_tank_design_parameters.tank_num_of_months_per_cycle), 'units': 'NUMBER'},
            'fish_per_tank_per_year': {'title': 'Total fish per tank per year','value': float(model_tank_design_parameters.fish_per_tank_per_year), 'units': 'NUMBER'},
        }
        ip_options={} 
        for i in investment_parameter_options_fish.keys():
            ip_options[i] =investment_parameter_options_fish[i].copy()

        for i in tank_design_parameters.keys():
            if 'num_of_tanks'==i:
                ip_options['initial_tanks_employed'].insert(0,float(model_tank_design_parameters.num_of_tanks))
            elif 'length'==i:
                ip_options['tank_length'].insert(0,float(model_tank_design_parameters.tank_length))
            elif 'width'==i:
                ip_options['tank_width'].insert(0,float(model_tank_design_parameters.tank_width))
            elif 'depth'==i:
                ip_options['tank_depth'].insert(0,float(model_tank_design_parameters.depth))
           
            elif 'total_fish_per_tank_per_cycle'==i:
                ip_options['fish_density'].insert(0,float(model_tank_design_parameters.total_fish_per_tank_per_cycle))
          
        
        for i in ['cost_of_land_per_sqm','cost_of_machinery_per_tank',
                         'cost_of_building_per_sqm','cost_of_unit_tank', 'total_land_required']:
          
            if 'cost_of_land_per_sqm'==i:
                ip_options['cost_of_land_per_sqm'].insert(0,float(model_tank_design_parameters.cost_of_land_per_sqm))
            elif 'cost_of_machinery_per_tank'==i:
                    ip_options['cost_of_machinery_per_tank'].insert(0,float(model_tank_design_parameters.machinery_cost_per_tank))
            elif 'cost_of_building_per_sqm'==i:
                    ip_options['cost_of_building_per_sqm'].insert(0,float(model_tank_design_parameters.building_cost_per_sqm))
            elif 'cost_of_unit_tank'==i:
                    ip_options['cost_of_unit_tank'].insert(0,float(model_tank_design_parameters.purchase_price_tank))
            
            elif 'total_land_required'==i:
                ip_options['total_land_required'].insert(0,float(model_tank_design_parameters.total_land_sqm))

        for i in ['cost_of_machinery']:
            first_ =ip_options[i][0]
            ip_options[i].insert(0,first_)
        # senoir debt
        ip_options['senior_debt_dynamic_parameter'].insert(0,para_senior_debt)
        #print(ip_options)

  


    
    breport= None
  
    #FishBusinessReport
    breport = FishBusinessReport(timing_assumptions=timing_assumptions, model_specifications=model_specifications, 
                        prices=prices, financing=financing, depreciation=depreciation_fish,  
                        working_capital=working_capital, taxes=taxes, macroeconomic_parameters =macroeconomic_parameters, 
                        tank_design_parameters =tank_design_parameters, investment_cost= investment_cost_fish
                        ,fish_business_options= fish_business_options, cost_real=cost_real_fish, 
                        investment_parameter_options=ip_options)
   

     #set descripton
    breport._set_model_description(user_model_decription)
   
    if not hasattr(breport, 'para_list_by_grad'):
        breport._sens_sensitivity_parrallel_generator()
        if hasattr(breport, 'para_list_by_grad'):
            input_vars= breport.para_list_by_grad
    else:
        input_vars= breport.para_list_by_grad
    
   
    #get user group credentials
    user_group_set =get_current_user_groups(request.user)
    premium_user = True if 'premium_user' in user_group_set else False

    if simulation_run and premium_user:
        if simulation_iterations>0:
            max_allowed=1000000
            min_allowed=100
            simulation_iterations=min(max(min_allowed,simulation_iterations),max_allowed)
            npv_bin_size=min(max(10,npv_bin_size),1000)
            #reseting
            request.session['count']=0
            request.session['total_runs']=simulation_iterations
            request.session.save()
            setattr(breport,'sim_count',0)

            breport._set_parameters_simulation(25)  
             #limit params
            if  total_params <=0:
                total_params=None 
                       
            graph_, ar ,employed_scenario_inputs = monteCarlo_sim(request,breport, npv_bin_size, 25, simulation_iterations, input_vars, total_params)
            setattr(breport,'npv_distribution' ,graph_)
            setattr(breport,'employed_scenario_inputs' ,employed_scenario_inputs)
    
    #add counter downloads
    create_downloads_instance(request, 'fish')
    create_user_model_downloads_instance(request, model_id)
    #get the spread sheet
    spread_Sht= breport.spreadsheet(request)

    #print(breport.__str__())
    return spread_Sht


