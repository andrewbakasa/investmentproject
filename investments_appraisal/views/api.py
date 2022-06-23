import datetime
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

import pandas as pd

from django.utils import formats

from trading.models import Investment, Investor



@login_required
def division_totals(request, dstart, dend):
    try:
        dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d')
        dend = datetime.datetime.strptime(dend, '%Y-%m-%d')
    except ValueError:
        return HttpResponseBadRequest(_('Invalid date format, expected yyyy-mm-dd'))
    res = Investment.objects.past().date_range(dstart, dend).order_by('division').values(
        'division').annotate(total=models.Sum('value'))
    if res:
        res = [(e['division'] or 'No division', abs(e['total'])) for e in res if e['total']]
        categories, total = zip(*res)
    else:
        categories, spent = [], []
    return JsonResponse({'categories': categories, 'total': total})
def get_data_points_releases(fail_or_real,
                    df, 
                    dstart=date.today() - timedelta(days=365),
                    dend=date.today(), 
                    steps=30):

    step = (dend - dstart) / steps
    #print('step interval: before:',step,'> ' ,steps)
    if step < timedelta(days=1):
        step = timedelta(days=1)
        steps = int((dend - dstart) / step)
    elif step > timedelta(days=30):
        step = timedelta(days=30)
        steps = int((dend - dstart) / step)

    #print('step interval: after:',step,'> ' ,steps)
    end_step = timedelta(days=30)
    #steps= 3
    data_dates = []  
    data_points = []  
    d1 = dstart
    d2 = d1 + end_step

    boo_loop= True
    while boo_loop:
        balance= 0 # reset every datapoint
        #---------------------DataFrame--------------------------------------
        if fail_or_real:
            df_fail = df.copy()
            df_fail.loc[:,'fail_date']=pd.to_datetime(df_fail.loc[:,'fail_date'])
            date_filter = (df_fail.fail_date >= str(d1)) & (df_fail['fail_date'] < str(d2))
            df2 = df_fail[date_filter]
        else:
            #---------------------Release--------------------------------------
            df_rel = df.copy()
            df_rel['rel_date'] = pd.to_datetime(df_rel['rel_date'], errors='coerce')
            df_rel=df_rel[~df_rel.isna()]
            df_rel['fail_date'] = df_rel['fail_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            date_filter =(df_rel.rel_date >= str(d1)) & (df_rel['rel_date'] < str(d2))
            df2 = df_rel[date_filter]
            #--------------------------------------------------
        balance= len(df2) # reset every datapoint
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

@login_required
def get_failures_releases_graph_by_rolling_month(request, dstart, dend):
    try:
        dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d').date()
        dend = datetime.datetime.strptime(dend, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest(_('Invalid date format, expected yyyy-mm-dd'))

    locomotives_df = pd.DataFrame(Investment.objects.all().values())	
    failures_df = pd.DataFrame(Investor.objects.all().values())
    locomotives_df['loco_id'] = locomotives_df['id']


    labels = []
    dataset = []
    if failures_df.shape[0]>0: #at least one invoices made 
         # merge
        df =pd.merge(locomotives_df, failures_df, on='loco_id').drop(['created_by_id_x',
                'approved_x', 'locked_x','date_created_x','created_by_id_y',
                'approved_y', 'locked_y','date_created_y','status_x', 'active_x','active_y',], axis=1).rename(
                    {'id_x': 'id', 'id_y': 'loco_failure_id','status_y': 'status'}, axis=1)
        dataset = []
        for bool_val in [True,False]:
            dates_, points_ = get_data_points_releases(bool_val,df, dstart, dend)
            if bool_val:
                val= 'Failures'
            else:
                val= 'Releases'
            dataset.append({'name':val , 'data': points_})
        if dataset:
            labels = [datetime.datetime.strftime(x, '%d %b %Y') for x in dates_]
        else:
            labels = []
        # print(dataset)
        # print(labels)
        return JsonResponse({'labels': labels, 'dataset': dataset}) 
    return JsonResponse({'labels': labels, 'dataset': dataset})     

