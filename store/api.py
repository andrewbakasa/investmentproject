import datetime

from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from store.utils import get_invoice_total

from .models import  Invoice, Company
import pandas as pd
#from strategicplan.utils import  get_invoice_total
@login_required
def get_sales_graph_by_day(request, dstart, dend):
    #print("here")
    try:
        dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d').date()
        dend = datetime.datetime.strptime(dend, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest(_('Invalid date format, expected yyyy-mm-dd'))

    company_df = pd.DataFrame(Company.objects.all().values())	
    sales_df = pd.DataFrame(Invoice.objects.all().values())
    
    if company_df.shape[0]>0: 
        company_df['company_id'] =company_df['id']
    #print("after stage 1")
    if sales_df.shape[0]>0: #at least one invoices made 
        df =pd.merge(company_df,sales_df, on='company_id').drop(['state','zip',
                'email', 'street','date_created'], axis=1).rename(
                    {'id_x': 'id', 'id_y': 'invoice_id'}, axis=1)
        
        df['total'] = df['invoice_id'].apply(lambda x: get_invoice_total(x))
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
       
     
       
        date_filter =(df['date'] >= str(dstart)) & (df['date'] <= str(dend))
        
        df = df[date_filter]
        
       
        df2 = df.groupby('date', as_index=False)['total'].agg('sum')
        #print(df2)
        get_sales_total(request,dstart,dend)
        return JsonResponse({'labels': df2['date'].tolist(), 'data': df2['total'].tolist()}) 

    return JsonResponse({'labels': [], 'data': []})     
	


@login_required
def get_sales_graph_by_month(request, dstart, dend):
    try:
        dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d').date()
        dend = datetime.datetime.strptime(dend, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest(_('Invalid date format, expected yyyy-mm-dd'))

    company_df = pd.DataFrame(Company.objects.all().values())	
    sales_df = pd.DataFrame(Invoice.objects.all().values())
    company_df['company_id'] =company_df['id']

    if sales_df.shape[0]>0: #at least one invoices made 
        df =pd.merge(company_df,sales_df, on='company_id').drop(['state','zip',
                'email', 'street','date_created'], axis=1).rename(
                    {'id_x': 'id', 'id_y': 'invoice_id'}, axis=1)
        
        df['total'] = df['invoice_id'].apply(lambda x: get_invoice_total(x))
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        df['year'] = pd.to_datetime(df['date']).dt.year
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day'] = pd.to_datetime(df['date']).dt.day
        
       
       
        date_filter =(df['date'] > str(dstart)) & (df['date'] < str(dend))
        
        df = df[date_filter]
        
        df2 = df.groupby('month', as_index=False)['total'].agg('sum')
       
        return JsonResponse({'labels': df2['date'], 'data': df2['total']}) 
        

# delete this supeded
def get_sales_total(request, dstart, dend):
    # try:
    #     dstart = datetime.datetime.strptime(dstart, '%Y-%m-%d').date()
    #     dend = datetime.datetime.strptime(dend, '%Y-%m-%d').date()
    # except ValueError:
    #     return HttpResponseBadRequest(_('Invalid date format, expected yyyy-mm-dd'))

    company_df = pd.DataFrame(Company.objects.all().values())	
    sales_df = pd.DataFrame(Invoice.objects.all().values())
    company_df['company_id'] =company_df['id']
    if sales_df.shape[0]>0: #at least one invoices made 
        df =pd.merge(company_df,sales_df, on='company_id').drop(['state','zip',
                'email', 'street','date_created'], axis=1).rename(
                    {'id_x': 'id', 'id_y': 'invoice_id'}, axis=1)
        
        df['total'] = df['invoice_id'].apply(lambda x: get_invoice_total(x))
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        df['year'] = pd.to_datetime(df['date']).dt.year
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day'] = pd.to_datetime(df['date']).dt.day
        

      
        date_filter =(df['date'] > str(dstart)) & (df['date'] < str(dend))
        
        df = df[date_filter]
      
        max_val = df['total'].max()
        min_val = df['total'].min()
        sum_total = df['total'].sum()
        aver_val = df['total'].mean()
      
        return  sum_total,max_val, aver_val, min_val



def get_sales_graph_pd(date_from,date_to,chart_type):
    company_df = pd.DataFrame(Company.objects.all().values())	
    sales_df = pd.DataFrame(Invoice.objects.all().values())
    company_df['company_id'] =company_df['id']

    if sales_df.shape[0]>0: #at least one invoices made 
        df =pd.merge(company_df,sales_df, on='company_id').drop(['state','zip',
                'email', 'street','date_created'], axis=1).rename(
                    {'id_x': 'id', 'id_y': 'invoice_id'}, axis=1)
        
        df['total'] = df['invoice_id'].apply(lambda x: get_invoice_total(x))
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        df['year'] = pd.to_datetime(df['date']).dt.year
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['day'] = pd.to_datetime(df['date']).dt.day
      

        
        df2 =df.groupby('date', as_index=False)['total'].agg('sum')
        df3 =df.groupby('month', as_index=False)['total'].agg('sum')
        df4 =df.groupby('year', as_index=False)['total'].agg('sum')
        
        date_from_df = datetime.datetime.strptime(date_from, '%m/%d/%Y')					
        date_to_df = datetime.datetime.strptime(date_to, '%m/%d/%Y')

        date_filter =(df['date'] > str(date_from_df)) & (df['date'] < str(date_to_df))
        
        df = df[date_filter]
        
        total_invoice = df['total'].sum()
        max_value = df['total'].max()
        min_value = df['total'].min()
        av_value = df['total'].mean()
        std_value = df['total'].std()
        row_max= all_data['total'].argmin(axis=0)

        df2 = df.groupby('date', as_index=False)['total'].agg('sum')
        print(df2)
        #get plot
        graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total'], data=df)
        return graph
  	