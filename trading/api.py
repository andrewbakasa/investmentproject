import datetime
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from trading.models import Investment
import pandas as pd

@login_required
def get_project_output_by_rolling_week(request,dstart, dend):

    try:
        dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d').date()
        dend = datetime.datetime.strptime(dend, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest(_('Invalid date format, expected yyyy-mm-dd'))

    
    #queryset = Project.objects.all()#filter(company__in=item_sbu)
    project_id = request.session['project_id']
    #print(project_obj)
    project = get_object_or_404(Investment, pk=project_id)
    qs=project.kpi_output_qs_released

    
    output_df = pd.DataFrame(qs.values())
    #print(output_df)	
   

    labels = []
    dataset = []
    last_data_14day=0
    if output_df.shape[0]>0: 
        dataset = []        
        dates_, points_ = get_data_points(output_df, dstart, dend)        
        dataset.append({'name':'7d rolling av.' , 'data': points_})
        
       
        av=0
        if len(points_)>0:
            av= sum(points_) / len(points_)
            av="{:.2f}".format(av)
        av_data_points = [av for num in range(len(points_))]
        
        #---------------
        full_span = get_date_span(dates_)
        dataset.append({'name':'Av_' + str(full_span)+ "d" , 'data': av_data_points})
        
        list_ =[]
        #convert from standard day into  item span
        days_list =[14,30,60,120]
        for i in days_list:
            val = get_item_span_from_date_span(dates_,i)
            #if not val in list_:
            list_.append(val)
        """ 
        print(days_list)
        print(list_) 
        """
        #others---
        last_data_14day= get_aggregate_rolling_averages_multiple(dates_,dataset,points_,list_,False)
        #--------------------------------------
        if dataset:
            labels = [datetime.datetime.strftime(x, '%d %b %Y') for x in dates_]
        else:
            labels = []
       
        return JsonResponse({'labels': labels, 'dataset': dataset ,'last_14day_dp':last_data_14day}) 
    return JsonResponse({'labels': labels, 'dataset': dataset,'last_14day_dp':last_data_14day}) 

def get_item_span_from_date_span(dates_,input_days_span):
    list_ =[]
    for i in range(len(dates_)):
        val = get_date_span(dates_,i+1)
        #print(val,input_days_span)
        if input_days_span <= val:
            return i+1
    return (len(dates_))
    
def get_aggregate_rolling_averages_multiple(dates_,dataset,points_, list_=[], verbose_=False):
     #----------------------------------
    iter=0
    last_data_14day=0
    for item_span in list_:
        iter+=1
        #skip all other point
        if item_span > len(points_):
            return
        val = get_date_span(dates_,item_span)
        if verbose_:
            print('list: ' + str(len(dates_))," date_span: " + str(val),
              '; list_size: '+ str(len(dates_)) , '; list_span'+ str(item_span)) 
            
        dyn_data_points = [cal_average_rolling(points_,iter, item_span) for iter in range(len(points_))] 
        if verbose_:
            print(dyn_data_points)
        # insert 11 at point before last
        if iter==1:
            last_data_14day= dyn_data_points[-1]

        dict_point ={'name':'Av_' + str(val)+ "d"  , 'data': dyn_data_points}
        last_index =len(dataset)-1
        if last_index >=0:
            dataset.insert(last_index, dict_point)
        else:
            dataset.append(dict_point)
    return last_data_14day
        #dataset.append({'name':'Av_' + str(item_span) + "n" + str(val)+ "d"  , 'data': dyn_data_points})
        #--------------------------------------
def get_date_span(dates_, splits=None):
    if splits==None:
        splits= len(dates_)
    if len(dates_)>0:
        if len(dates_)>=splits:
            ub= min(splits,len(dates_)-1)
            date_span=dates_[ub]-dates_[0]
            return(date_span.days)
        else:
            return get_date_span(dates_, len(dates_))
    else:
        return 0   
def get_average(list_,start, end):
    #1 & 2 diff 2-1 =1 but have two items
    splice_size = end - start + 1
    ub=len(list_)
    upper_bound= min(end+1,ub)
    total = 0
    for i in range(start, upper_bound):
        total += list_[i]
    if splice_size>0:
        av=total/splice_size
        return  "{:.2f}".format(av)
    return 0

def cal_average_rolling(list_,iter_, span_):
    len_ =len(list_)
    mod_ =(iter_) % (span_)   
    start=iter_- mod_   
    end   =  start + span_-1
    #print(iter_,mod_, span_, start, end)
    return get_average(list_,start, min(end, len_))
    

def get_data_points(df, 
                    dstart=date.today() - timedelta(days=365),
                    dend=date.today(), 
                    steps=30, period=7):

    step = (dend - dstart) / steps
    #print('step interval:',step)
    if step < timedelta(days=1):
        step = timedelta(days=1)
        steps = int((dend - dstart) / step)
    elif step > timedelta(days=30):
        step = timedelta(days=30)
        steps = int((dend - dstart) / step)


    end_step = timedelta(days=period)
    #steps= 3
    data_dates = []  
    data_points = []  
    d1 = dstart
    d2 = d1 + end_step

    boo_loop= True
    while boo_loop:
        balance= 0 # reset every datapoint
        #---------------------DataFrame--------------------------------------
       
        df_fail = df.copy()
        df_fail.loc[:,'date_created']=pd.to_datetime(df_fail.loc[:,'date_created'])
        date_filter = (df_fail.date_created >= str(d1)) & (df_fail['date_created'] < str(d2))
        df2 = df_fail[date_filter]
        #print(df.columns)
        balance=float(df2['value'].sum()) #len(df2) # reset every datapoint
        data_dates.append(d1)
        data_points.append(balance)
        #---------
        d1 += step
        d2 = d1 + end_step

        #-----include last day point if not there already
        if d1 > dend and d1-step < dend :
            d1 = dend 
        elif d1 > dend:
            #terminate if condition satisfied
            boo_loop= False
    return data_dates,data_points
