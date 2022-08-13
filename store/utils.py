import json

from common.utils import short_month_from_int_to_string, short_weekday_from_int_to_string

from .models import *
from .models import Customer

# create cart for guest user
def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    #print('Cart:', cart)

    orderitems = []

    # the html will be expecting a variable called order
    # initialize a dictionary with the expected keys
    # which will be viewed as an object
    # with attributes corresponding to the keys
    order = {'total_quantity': 0, 'total_price': 0, 'shipping': False}
    total_quantity = order['total_quantity']

    for i in cart:
        try:
            current_quantity = cart[i]['quantity']
            #print(current_quantity)
            total_quantity += current_quantity
            #print(total_quantity)

            product = Product.objects.get(id=i)
            total_price = (product.price * current_quantity)

            order['total_price'] += total_price

            orderitem = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': current_quantity,
                'total': total_price
            }
            orderitems.append(orderitem)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    #print(total_quantity)

    order['total_quantity'] = total_quantity

    return {
        'total_quantity': total_quantity,
        'order': order,
        'orderitems': orderitems
    }

# handle user or guest actions
# return appropriate cart data
def cart_data(request):
    if request.user.is_authenticated:
        #customer = request.user.customer
        customer, created = Customer.objects.get_or_create(
            user=request.user,
        )
        if created:
            customer.name=request.user.username
            customer.email=request.user.email
       

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
        total_quantity = order.total_quantity
    else:
        cookie_data = cookie_cart(request)
        total_quantity = cookie_data['total_quantity']
        order = cookie_data['order']
        orderitems = cookie_data['orderitems']

    return {
        'total_quantity': total_quantity,
        'order': order,
        'orderitems': orderitems
    }

def guest_order(request, data):
    # print('User is not logged in.')

    # print('COOKIES: ', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    data = cookie_cart(request)
    orderitems = data['orderitems']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False,
    )

    for orderitem in orderitems:
        product = Product.objects.get(id=orderitem['product']['id'])

        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=orderitem['quantity']
        )

    return customer, order

import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

from .models import Invoice, Expense
from django.shortcuts import get_object_or_404 
import numpy as np
import pandas as pd
#from .lib import short_month_from_int_to_string , short_weekday_from_int_to_string

def get_image():
    # create a byte buffer for image to save
    buffer = BytesIO()
    #create the plot with the use of BytesIO object as its is 'file'
    plt.savefig(buffer, format='png')
    # set the cursor the begining of the stream
    buffer.seek(0)
    # retrieve the entire contnent of the 'file'
    image_png =buffer.getvalue()

    graph = base64.b64encode(image_png)
    
    #print(graph)
    graph= graph.decode('utf-8')
    # free the memory of the buffer
    buffer.close()
    return graph


def get_unique_ordered_months(months_list):
    Months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    new_list=[]
    for i in Months:
        if i in months_list:
            new_list.append(i)
    return  new_list           

def get_simple_plot(chart_type, *args, **kwargs):
    #https://matplotlib.org/faq/usage_faq.html?highlight=backend#what-is-a-backend
    plt.switch_backend('agg')
    fig =plt.figure(figsize=(8,4))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    data2 = kwargs.get('data2')
    dataProd = kwargs.get('dataProd')
    

   

    if chart_type =='barplot':
        print(data2)
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day
        data2['month'] = data2['month'].apply(lambda x: short_month_from_int_to_string(int(x)))

      
        # ordered months list
        ordered_months= get_unique_ordered_months(data2.month.unique())

        title = 'Monthly Sales [USD]'
        plt.title(title)

        fig, axes = plt.subplots(1,2, figsize=(10,4))
        
        #-------AXES 01--------------------------
        axes[0].set_title(title + ' Aggregate ')
        sns.set_style('whitegrid')
        #sns.barplot("month", 'total',data=data2, order=ordered_months,ax=axes[0])
        sns.barplot('month','total', hue='status', data=data2, order=ordered_months, ax=axes[0])
        sns.set_context('paper',font_scale=1.0)
        sns.set_style('whitegrid')

        #-------AXES 02--------------------------
        axes[1].set_title(title + ' Company')
        sns.barplot(data2['month'],data2['total'], hue='name', data=data2,order=ordered_months, ax=axes[1])

    elif chart_type =='boxplot':
        # proper to compare sales per week/ month for each company
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day
        data2['month'] = data2['month'].apply(lambda x: short_month_from_int_to_string(int(x)))
        
        title = 'Invoiced Sales'
        sns.set_style('whitegrid')

        fig, axes = plt.subplots(1,2, figsize=(10,4))

         # ordered months list
        ordered_months= get_unique_ordered_months(data2.month.unique())
       
        #-------AXES 01------------------------------
        axes[0].set_title('Box Plot Agregate')
        #sns.boxplot("month", 'total',data=data2, order=ordered_months,ax=axes[0])
        sns.boxplot("month", 'total',hue='status',data=data2, order=ordered_months,ax=axes[0])
       
        #--------AXES 02------------------------------
        axes[1].set_title('Box Plot: Company')
        sns.boxplot(x='month', y='total', data=data2, order=ordered_months, hue='name', ax=axes[1])
        sns.set_context('paper',font_scale=1.0)
        plt.legend(loc=0)
        plt.title(title)
    elif chart_type =='countplot':
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        #data2['month'] = data2['date'].dt.strftime('%b')
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day
        data2['month'] = data2['month'].apply(lambda x: short_month_from_int_to_string(int(x)))
        
      
        sns.set_style('whitegrid')
          
        fig, axes = plt.subplots(1,2, figsize=(10,4))
         # ordered months list
        ordered_months= get_unique_ordered_months(data2.month.unique())
        
        #-------AXES 01----------------
        axes[0].set_title('Count Plot Agregate')
        sns.countplot(x="month", data=data2,order=ordered_months,
                    hue='status',ax=axes[0])
        
        #---------AXES 02------------
        axes[1].set_title('Count Plot Company')
        sns.countplot(x="month", data=data2,order=ordered_months,
                    hue='name',ax=axes[1])
       
        sns.set_context('paper',font_scale=1.0)
    elif chart_type =='lineplot':
        title = 'Invoiced Sales'
        plt.title(title)
        plt.plot(x,y)
    elif chart_type =='heatmap':
        title = 'Invoiced Sales'
        plt.title(title)
        data_matrix= data2.corr()
        sns.heatmap(data_matrix, annot=True, cmap='Blues')
        sns.set_context('paper',font_scale=1.0)
    elif chart_type =='subplot':
       #data2['month'] = pd.to_datetime(df['date'], format='%m').dt.month_name().str.slice(stop=3)
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        #data2['month'] = data2['date'].dt.strftime('%b')      
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day
        data2['weekday'] = pd.DatetimeIndex(data2['date']).weekday

        data2['month'] = data2['month'].apply(lambda x: short_month_from_int_to_string(int(x)))
        data2['weekday'] = data2['weekday'].apply(lambda x: short_weekday_from_int_to_string(int(x)))

        title = 'Invoiced Sales'
        fig, axes = plt.subplots(3,3, figsize=(14,8))
       
         # ordered months list
        ordered_months= get_unique_ordered_months(data2.month.unique())
       
        # set categorical order
        data2['month'] = pd.Categorical(data2['month'],
                                   categories=ordered_months,
                                   ordered=True)
        ordered_weekdays=["sun","mon","tues","wed","thur","fri","sat"]                           
        data2['weekday'] = pd.Categorical(data2['weekday'],
                                   categories=ordered_weekdays,
                                   ordered=True)                           

        rr= sns.lineplot(x=data2['month'],y=data2['total'], data=data2, ax=axes[0,0])


        axes[0,1].set_title('Scatter Plot')
        sns.scatterplot(data2['month'],data2['total'], 
                hue=data2['company_id'], s=100, ax=axes[0,1]) 

        axes[0,2].set_title('Histogram')
        """axes[0,2].hist(data2['de6'], data2['de9'],
           bins=np.arange(2, 5, 0.25), stacked=True)"""
        #axes[0,2].legend(['','',''])
        axes[0,2].hist(data2['company_id'],
           bins=np.arange(1, 5, 0.25))
        axes[1,0].set_title('Bar Plot')
        sns.barplot(data2['month'],data2['total'], hue='company_id', data=data2, ax=axes[1,0])

        axes[1,1].set_title('Week')        
        days_in_week = data2.pivot_table(index="day", columns="week", values="total", aggfunc='sum')
        rp= sns.heatmap(days_in_week, annot=True, cmap='RdYlGn', linewidths=.5, ax=axes[1,1])
        rp.set_yticklabels(rp.get_yticklabels(), rotation=0, horizontalalignment='right') 
        
        axes[1,2].set_title('Day_in_Month')
        days_in_month = data2.pivot_table(index="day", columns="month", values="total", aggfunc='sum')
        rs= sns.heatmap(days_in_month, annot=True, cmap='RdYlGn', linewidths=.5, ax=axes[1,2])
        rs.set_yticklabels(rs.get_yticklabels(), rotation=-0 )
        
        axes[2,0].set_title('HeatMap')
        months_in_year = data2.pivot_table(index="month", columns="year", values="total", aggfunc='sum')
        sns.heatmap(months_in_year, cmap='RdYlGn',  linewidths=.5, ax=axes[2,0])
       
        axes[2,1].set_title('Count')
        ra= sns.countplot(x="date", data=data2,
                    facecolor=(0, 0, 0, 0),
                    linewidth=5,
                    edgecolor=sns.color_palette("dark", 3),ax=axes[2,1] )

        ra.set_xticklabels(ra.get_xticklabels(), rotation=45, horizontalalignment='right')              


        axes[2,2].set_title('Week_Day')
        
        week_day = data2.pivot_table(index="weekday", columns="month", values="total", aggfunc='sum')
        rs= sns.heatmap(week_day, annot=True, cmap='RdYlGn', linewidths=.5, ax=axes[2,2])
        rs.set_yticklabels(rs.get_yticklabels(), rotation=-0 )
        
        plt.title(title)
        plt.tight_layout(pad=1)
        sns.set_context('paper',font_scale=1.0)

    elif chart_type =='jointplot':
        title = 'Invoiced Sales'
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day
        data2['weekday'] = pd.DatetimeIndex(data2['date']).weekday
        
        sns.set_style('whitegrid')
       
        # plt.title(title)
        fig, axes = plt.subplots(1,2, figsize=(14,8))

        axes[0].set_title("week")
        sns.jointplot(data=data2, x="week", y="total", hue="name", ax=axes[0])
       
        sns.set_context('paper',font_scale=1.0)
        axes[1].set_title("month")
        sns.jointplot(data=data2, x="month", y="total", hue="name", ax=axes[1])
        plt.tight_layout(pad=1)
        

  
    elif chart_type =='pairplot':
        title = 'Invoiced Sales'
        sns.set_style('whitegrid')
        plt.figure(figsize=(10,4))
        sns.pairplot(data2, hue='company_id', palette='Blues')
        sns.set_context('paper',font_scale=1.0)
        plt.title(title)
    elif chart_type =='pairgrid':
        title = 'Invoiced Sales'
        sns.set_style('whitegrid')
        plt.figure(figsize=(10,4))
        plt.title(title)
        grid= sns.PairGrid(data2)
        grid.map_diag(plt.hist)
        grid.map_offdiag(plt.scatter)
        sns.set_context('paper',font_scale=1.0)
    elif chart_type =='scatterplot':
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        #data2['month'] = data2['date'].dt.strftime('%b')
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day

              
        data2['month'] = data2['month'].apply(lambda x: short_month_from_int_to_string(int(x)))
        title = 'Invoiced Sales'
        sns.set_style('whitegrid')
        plt.title(title)
         # ordered months list
        ordered_months= get_unique_ordered_months(data2.month.unique())#order=ordered_months, 
        grid = sns.FacetGrid(data=data2,col = "name", hue = "name", col_wrap=3)
        grid.map(sns.scatterplot, "month", "total")
        grid.add_legend()
        plt.tight_layout()
        sns.set_context('paper',font_scale=1.0)

    elif chart_type =='violinplot':
        data2['year'] = pd.DatetimeIndex(data2['date']).year
        data2['month'] = pd.DatetimeIndex(data2['date']).month
        #data2['month'] = data2['date'].dt.strftime('%b')
        data2['week'] = pd.DatetimeIndex(data2['date']).week
        data2['day'] = pd.DatetimeIndex(data2['date']).day

              
        data2['month'] = data2['month'].apply(lambda x: short_month_from_int_to_string(int(x)))
        title = 'Invoiced Sales'
        sns.set_style('whitegrid')
         # ordered months list
        ordered_months= get_unique_ordered_months(data2.month.unique())

        

        fig, axes = plt.subplots(1,2, figsize=(14,8))
        
        #----------------AXES 02----------------------------------
        axes[0].set_title(title + " [paid/unpaid]")
        sns.violinplot(x='month', y='total', data=data2,order=ordered_months, hue="status", ax=axes[0])

        #-------AXES 02---------------
        axes[1].set_title(title )
        sns.violinplot(x='month', y='total', data=data2,order=ordered_months, ax=axes[1])


        sns.set_context('paper',font_scale=1.0)
    
    elif chart_type =='products':
        productsales = dataProd.groupby('product_name').sum()
        print(dataProd)
        print(productsales)
        fig =plt.figure(figsize=(15,7))
        #product= dataProd['product_name'].unique()
        products =[product for product, df in dataProd.groupby('product_name')]
        plt.bar(products, productsales['totalprice'])
        plt.xticks(products, rotation='vertical' , size=6)
        plt.ylabel('Sales in $')
        plt.xlabel('Product Name')
    else:
        title = 'Invoiced Sales'
        plt.title(title)
       
      
        title = 'Invoiced Sales'
        sns.set_style('whitegrid')
        plt.figure(figsize=(10,4))
        plt.title(title)
        grid= sns.PairGrid(data2)
        grid.map_diag(plt.hist)
        grid.map_offdiag(plt.scatter)
        sns.set_context('paper',font_scale=1.0)


    graph = get_image()

    return graph
        

def get_invoice_total(invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    total = invoice.total_items()
    #print(total)
    return float(total)

def get_expense_total(id):
    expense = get_object_or_404(Expense, pk=id)
    total = expense.total()
    #print(total)
    return float(total)

""" 
Save multiple plots to one pdf file
Many image file formats can only have one image per file, but some formats support multi-page files. Currently only the pdf backend has support for this. To make a multi-page pdf file, first initialize the file:

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage.pdf')
You can give the PdfPages object to savefig(), but you have to specify the format:

plt.savefig(pp, format='pdf')
An easier way is to call PdfPages.savefig:

pp.savefig()
Finally, the multipage pdf object has to be closed:

pp.close()
The same can be done using the pgf backend:

from matplotlib.backends.backend_pgf import PdfPages """

""" 
import pandas as pd

df = pd.DataFrame({'client':['sss', 'yyy', 'www'], 'Month': ['02', '12', '06']})

look_up = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May',
            '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

df['Month'] = df['Month'].apply(lambda x: look_up[x])
df

  Month client
0   Feb    sss
1   Dec    yyy
2   Jun    www """

""" 
For anyone who is still interested in the difference between pivot and pivot_table, there are mainly two differences:

pivot_table is a generalization of pivot that can handle duplicate values for one pivoted index/column pair. Specifically, you can give pivot_table a list of aggregation functions using keyword argument aggfunc. The default aggfunc of pivot_table is numpy.mean.
pivot_table also supports using multiple columns for the index and column of the pivoted table. A hierarchical index will be automatically generated for you.
REF: pivot and pivot_table

I debugged it a little bit.

The DataFrame.pivot() and DataFrame.pivot_table() are different.
pivot() doesn't accept a list for index.
pivot_table() accepts.
Internally, both of them are using reset_index()/stack()/unstack() to do the job.

pivot() is just a short cut for simple usage, I thin 
"""