

import json
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
import os
import numpy as np
from datetime import datetime, date
import pandas as pd
from dateutil.relativedelta import relativedelta
import decimal
import pandas as pd
import functools
from django.http import HttpResponseRedirect
import math



from .models import *
import numpy as np
import os

from django.contrib.auth.models import User

from dateutil import rrule
import datetime

def exponent_rump_target(target,actual):
    #----------------
    #------------------
    #--------------------
    #-----------------------
    #----------------------------
    #--------------------------------
    #-------------------------------------
    #Throughput , the lower the better
    if actual <=target:
        return 1
    else:
        # x is negative
        x = target-actual
        u=10
        return math.exp(x/u)

def weeks_between(start_date, end_date):
    weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
    return weeks.count()

def get_project_outputs_monthly(request, dstart, dend, context):

    outstanding= context['outstanding']
    project_id = request.session['project_id']
    project = get_object_or_404(Investment, pk=project_id)#['id'])
    #throughput_target=10# float(project.throughput_target)
    # project budget
    budget_= float(project.total_value)
    throughput_target=budget_
    #---ending date
    due_date= project.closing_date
    
    #---purchase orders funding
    """  
    po_funding_dict= project.purchase_orders_funding_dict

    """
    #material:no_po, not_funded, funded
    #material_funding_dict= project.material_items_count_dict

    weekly_output_target= float(project.weekly_output_target)
    qs=project.kpi_output_qs
    qs_engaged=project.kpi_output_qs_released
    qs_wip=project.kpi_output_qs_wip
    output_df = pd.DataFrame(qs.values())
    output_wip_df = pd.DataFrame(qs_wip.values())
    output_engaged_df= pd.DataFrame(qs_engaged.values())
    if output_df.shape[0]> 0 : 
      
        output_df['date_status_changed'] = pd.to_datetime(output_df['date_status_changed'])
        output_df['date_created'] = pd.to_datetime(output_df['date_created'])       
        ave_throughput = context['engaged']# 11#throughput_get_mean(output_df)
        
        #--------------------GET AVERAGE Weekly Output--------------------
        total_releases=context['engaged'] if context['engaged'] else 0
        date_1 =context['minus_full_period'] if context['minus_full_period'] else 0
        date_2 = timezone.now()



        num_of_weeks=weeks_between(date_1,date_2) + 1
        #print(date_1,date_2,num_of_weeks)
        ave_weekly_output=total_releases/num_of_weeks if num_of_weeks !=0 else 0
        ave_weekly_output = '{:.2f}'.format(ave_weekly_output)
        #------------------------------------------------
        outputs_wip, total_underrepairs=underrepairs(output_wip_df)
        #print(total_underrepairs)
        context['outputs_wip'] = outputs_wip
        context['wip'] = total_underrepairs

        #print(outputs_wip)
        # 1-------------------
        assets_admission, total_admissions_this_month= admissions(output_wip_df,dstart,dend)
        #2------------------------------
        releases_outputs, total_rel_this_month= outputs_releases(output_engaged_df,dstart,dend)       
      
        context['admissions'] = total_admissions_this_month
        context['assets_admission'] = assets_admission
        context['releases'] = total_rel_this_month
        context['releases_outputs'] = releases_outputs
        context['difference'] =  context['releases']- context['admissions']


        #--------last month ADMISSIONS & OUTPUTS...............................
        #dt = dstart.replace(tzinfo=None)
        previous_last = dstart - timedelta(days=1)
        previous_first = previous_last.replace(day=1)        
       
       
        # 3-------------------
        previous_assets_admission, total_admissions_last_month= admissions(output_wip_df,previous_first,previous_last)
      
        #4------------------------------
        previous_releases_outputs, total_rel_last_month= outputs_releases(output_engaged_df,previous_first,previous_last)
         
        # context['outputs_wip'] = outputs_wip
        context['previous_admissions'] = total_admissions_last_month
        context['previous_assets_admission'] = previous_assets_admission
        context['previous_releases'] = total_rel_last_month
        context['previous_releases_outputs'] = previous_releases_outputs
        context['previous_difference'] =  context['previous_releases']- context['previous_admissions']
       
        #context['today'] =  #timezone.now()


        context['last_month'] = previous_first
        context['past'] = date.today() - timedelta(days=60)
        #Project Analytics
        context['dict_kpi'] = get_kpi_dict(throughput_target,ave_throughput,
                                         weekly_output_target, ave_weekly_output, due_date,outstanding)
       
        # procurement
        #context['dict_procurement'] = get_procurement_dict(budget_,po_funding_dict,material_funding_dict)
    return context 
def get_procurement_dict(budget_,po_funding_dict, material_funding_dict):
    
    orders_funded=po_funding_dict['funded']
    orders_unfunded=po_funding_dict['unfunded']


    materials_no_po=material_funding_dict['no_po']
    materials_not_funded=material_funding_dict['not_funded']
    materials_funded=material_funding_dict['funded']
    dict_kpi =[]

    
    dict_ ={}
    dict_['name']= 'Budget'
    dict_['target']= float(budget_)#float(7)
    dict_['actual']= float(orders_funded)
    dict_['actualPercent']= float(dict_['actual'])/ float(dict_['target']) if  dict_['target'] !=0 else 1
    dict_['percent']=dict_['actualPercent']*100
    dict_['lessThan50Percent']= (0.5 * dict_['target'])> float(dict_['actual'])
    dict_kpi.append(dict_)



    dict_ ={}
    dict_['name']= 'P/O Funded'
    dict_['target']= float(orders_funded)+float(orders_unfunded)
    dict_['actual']= float(orders_funded)
    dict_['actualPercent']= float(dict_['actual'])/ float(dict_['target']) if  dict_['target'] !=0 else 1
    dict_['percent']=dict_['actualPercent']*100
    dict_['lessThan50Percent']= (0.5 * dict_['target'])> float(dict_['actual'])
    dict_kpi.append(dict_)

    dict_ ={}
    dict_['name']= 'Material Funded'
    dict_['target']= float(materials_not_funded + materials_funded)
    dict_['actual']= float(materials_funded)
    dict_['actualPercent']= float(dict_['actual'])/ float(dict_['target']) if  dict_['target'] !=0 else 1
    dict_['percent']=dict_['actualPercent']*100
    dict_['lessThan50Percent']= (0.5 * dict_['target'])> float(dict_['actual'])
    dict_kpi.append(dict_)

    dict_ ={}
    dict_['name']= 'Material No P/O'

   
    dict_['target']= 0 #float(materials_no_po + materials_not_funded + materials_funded)
    dict_['actual']= float(materials_no_po )
    percent_performance= exponent_rump_target(float(dict_['target']),float(dict_['actual']))
    dict_['actualPercent']= float(percent_performance)
    dict_['percent']=0#dict_['actualPercent']*100
    dict_['lessThan50Percent']= 0.5 > float(dict_['actualPercent'])
    dict_kpi.append(dict_)

    return dict_kpi

def get_kpi_dict(throughput_target,ave_throughput,
                 weekly_output_target,ave_weekly_output, due_date, outstanding):
    dict_kpi =[]

    
    dict_ ={}
    dict_['name']= 'Required Funds'
    dict_['target']= throughput_target#float(7)
    dict_['actual']= ave_throughput
    
    percent_performance= exponent_rump_target(float(dict_['target']),float(dict_['actual']))
    dict_['actualPercent']= float(percent_performance)
    dict_['lessThan50Percent']= 0.5 > float(dict_['actualPercent'])
    dict_kpi.append(dict_)



    dict_ ={}
    dict_['id']= 'weekly_out_put'
    dict_['name']= 'Weekly Inflows'
    dict_['target']= weekly_output_target #float(10)
    dict_['actual']= ave_weekly_output
    dict_['actualPercent']= float(dict_['actual'])/ float(dict_['target']) if  dict_['target'] !=0 else 1
    dict_['lessThan50Percent']= (0.5 * dict_['target'])> float(dict_['actual'])
    dict_kpi.append(dict_)

    dict_ ={}
    days_left = (due_date-date.today()).days
    weeks= weeks_between(date.today(), due_date)

    if days_left>0:
        if outstanding>0:
            production_rate_desired= outstanding/weeks  if weeks>0 else outstanding
        else:
            production_rate_desired=0
    else:
        production_rate_desired=outstanding

    
    dict_['id']= 'desired_rate'
    dict_['name']= f'Desired inflow rate @time left({days_left}days)'
    dict_['target']= float(production_rate_desired) #float(10)
    dict_['actual']= ave_weekly_output
    dict_['actualPercent']= float(dict_['actual'])/ float(dict_['target']) if  dict_['target'] !=0 else 1
    dict_['lessThan50Percent']= (0.5 * dict_['target'])> float(dict_['actual'])
    dict_kpi.append(dict_)

    return dict_kpi
def throughput_get_mean(df):
    output_df =df.copy()
    mask_under_repair = (output_df['rel_date'].isna()) 
    mask_admission_NotNA = ~(output_df['admission_date'].isna())
    mask_releases_NotNA = ~(output_df['rel_date'].isna())
    mask_under_repair =mask_under_repair & mask_admission_NotNA

    #--------------------GET AVERAGE THROUGHPUT--------------------
    mask_admitted_then_released =mask_admission_NotNA & mask_releases_NotNA
    df_thru = output_df[mask_admitted_then_released]
    
   
    df_thru['repairtime'] =  (df_thru['rel_date']- df_thru['admission_date']).dt.days
    if len(df_thru)>0:
        ave_throughput= df_thru["repairtime"].mean()
        ave_throughput = '{:.2f}'.format(ave_throughput)
    else:
        ave_throughput=0

    return ave_throughput

def underrepairs(df): 
    outputs_wip =[]
    total=0
    if df.shape[0]> 0 : 
        output_df =df.copy()
        #print(df)
        output_df['date_created'] = pd.to_datetime(output_df['date_created'])
        df_urepair= output_df.sort_values(by=['date_created'],ascending=False)
        
       
        total = float(df_urepair['value'].sum())

    
    # for i in range(len(df_urepair)):
    #     x={}
        
    #     x['name']=df_urepair.iloc[i,:]['id_num']
    #     date_ = df_urepair.iloc[i,:]['admission_date']
    #     if not (date_==date_):
    #         date_= 'No given'
    #     x['date'] = date_
    #     exp_rel_date_ = df_urepair.iloc[i,:]['exp_rel_date']
    #     if not (exp_rel_date_==exp_rel_date_):
    #         exp_rel_date_= 'No given'
    #     x['date2'] = exp_rel_date_
    #     x['text'] = df_urepair.iloc[i,:]['category']
        
    #     outputs_wip.append(x)
    return outputs_wip, total


def admissions(df,dstart, dend):
    
    assets_admission =[]
    total_admissions=0
    if df.shape[0]> 0 : 
        output_df =df.copy()
        #print(df)
        output_df['date_created'] = pd.to_datetime(output_df['date_created'])
        date_filter =(output_df['date_created'] >= str(dstart)) & (output_df['date_created'] <= str(dend))
        df_admit = output_df[date_filter].sort_values(by =['date_created'],ascending=False) 
        df_admit['date_created'] = pd.to_datetime(df_admit['date_created'])

        total_admissions = float(df_admit['value'].sum())
        assets_admission =[]

        # #print(1,df_admit)
        # for i in range(len(df_admit)):
        #     x={}
        #     x['name']=df_admit.iloc[i,:]['id_num']
        #     x['date'] = df_admit.iloc[i,:]['admission_date']
        
        #     rel_date_ = df_admit.iloc[i,:]['rel_date']
        #     if not (rel_date_==rel_date_):
        #         rel_date_= 'No Released Yet'
        #     x['date2'] = rel_date_
        #     x['text'] = df_admit.iloc[i,:]['category']
        #     assets_admission.append(x)    
   
    return  assets_admission, total_admissions

def outputs_releases(df,dstart, dend):
    releases_outputs =[]
    total_rel=0
    if df.shape[0]> 0 :
        output_df =df.copy()
        #print(output_df)
        output_df['date_created'] = pd.to_datetime(output_df['date_created'])
        date_filter =(output_df['date_created'] >= str(dstart)) & (output_df['date_created'] <=  str(dend))
        df_rel = output_df[date_filter].sort_values(by=['date_created'],ascending=False)
        
    
    
        total_rel = float(df_rel['value'].sum())
        
        
        releases_outputs =[]
    # for i in range(len(df_rel)):
    #     x={}
    #     x['name']=df_rel.iloc[i,:]['id_num']
    #     x['date']=df_rel.iloc[i,:]['rel_date']
    #     x['text'] = df_rel.iloc[i,:]['category']
    #     x['downtime'] = df_rel.iloc[i,:]['downtime']
        
    #     releases_outputs.append(x) 
    
   
    return  releases_outputs, total_rel
