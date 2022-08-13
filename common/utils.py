import datetime
import pandas as pd


def get_current_user_groups(user):
    user_set=[]
    if user.groups.exists():
        user_set = list(user.groups.values_list('name',flat = True)) 
    return user_set
	
def clip_trailing_chars(inputstr, max_len=25):
    return "{}{} ".format(inputstr[:max_len], "... " if len(inputstr)> max_len else "")


months_short_names= {1: "Jan", 2: "Feb", 3: "Mar", 4: "April", 
				5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
				9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}


months_long_names= {1: "Jan", 2: "Feb", 3: "Mar", 4: "April", 
				5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
				9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"} 
def stringfy_list(list_, comma_=','):
	#list1 = ['1', '.2', '3']
	#covert float to string
	if isinstance(list_,list):
		list_=[str(x) for x in list_] 
		
	str1 = str(comma_).join(list_)
	return str1

def de_stringfy_tolist(str_, comma_=','):
	#list1 = ['1', '.2', '3']
	return str_.split(comma_) 
def long_date(x):
	#x= datetime.datetime(x.year, x.month, x.day)
	if type(x)==str:
		x = datetime.datetime.strptime(x, '%Y-%m-%d').date()
    
	#return datetime.datetime.strftime(x, '%d %b %Y') # 21 Aug 2021

	return get_long_date_from_str(x)# if x is empty



def get_long_date_from_str(x):
	if (type(x) ==datetime.date or 
		type(x)==pd._libs.tslibs.timestamps.Timestamp) :
		return x.strftime('%d %b %Y') # 21 Aug 2021
	return x  

def long_time(x):
	if (type(x) ==datetime.time or 
		type(x)==pd._libs.tslibs.timestamps.Timestamp) :
		return x.strftime('%r') # 16:10  datetime.datetime.strftime(x, '%r')#
	return x 

def thousand_sep(num):
	#return ("{:,}".format(num))    # For Python ≥2.7
	return (f'{num:,}')          # For Python ≥3.6
	
    
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def short_month_name(item):
    month_list = ['Jan', "Feb", "Mar", "Apr", "May", "Jun", "Jul" , "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    if int(item)> 0 and int(item) <= len(month_list):
        return month_list[int(item)-1]
    return item

import datetime


Quarters = {"Q1": 'First Quarter', "Q2": 'Second Quarter', "Q3": 'Third Quarter', "Q4": 'Fourth Quarter',}
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    date_x = next_month - datetime.timedelta(days=next_month.day)
    # remove time part
    if (type(date_x) == datetime.datetime):
        return date_x.date()
    return date_x
     

def format_month(mon):
    if mon < 10 :
        return str("0"+ str(mon))
    else:
        return str(mon)

def get_dates(year, period="Annual"):
    
    if period in ("Q1","Q2", "Q3", "Q4"):
        x = get_period_as_int(period)
        y = x-1
        z = y*3
        date1 =  str(year) +  "-" + format_month(z + 1) + "-01" 
        date2 =  str(year) + "-" + format_month(z + 3) + "-01"
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        date2 = last_day_of_month(date2)
        return date1, date2
    elif period in ("H1","H2"):
        x = get_period_as_int(period)
        y = x-1
        z = y*6
        date1 =  str(year)  + "-" + format_month(z + 1) + "-01"
        date2 =  str(year)  + "-" + format_month(z + 6) + "-01"
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        date2 = last_day_of_month(date2)
        return date1, date2
    elif period in ("Annual"):
        x = get_period_as_int(period)
        y = x-1
        z = y*12
        date1 =  str(year)  + "-" + format_month(z + 1) + "-01"
        date2 =  str(year)  + "-" + format_month(z + 12) + "-01"
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        date2 = last_day_of_month(date2)
      
        return date1, date2


def get_dates_period(year, quarter, month, week, day):
    # under constructuion, 
    # edit week
    # edit date
    # last update 12 Feb 2021 
    #print("lib:in get period : Y: " + year + " Q:" +  quarter + " M:" +month )
    if  month is not None and len(month)>0:
        x = month_from_string_to_int(month)
        date1 =  str(year) +  "-" + format_month(x) + "-01" 
        date2 =  str(year) + "-" + format_month(x) + "-01"
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        date2 = last_day_of_month(date2)
        return date1, date2, month_from_int_to_string(x)

   # elif  quarter in ("Q1","Q2", "Q3", "Q4"):
    else:
       
        x = get_period_as_int(quarter)
      
        y = x-1
        z = y*3
        date1 =  str(year) +  "-" + format_month(z + 1) + "-01" 
        date2 =  str(year) + "-" + format_month(z + 3) + "-01"
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d")
        date2 = last_day_of_month(date2)
        return date1, date2, quarter #Quarters[quarter]
        
        
def get_array_months_for_period_input(period):
    if period =="Q1":
        return ['January', 'February','March']
    elif period =="Q2":
        return ['April', 'May','June']
    elif period =="Q3":
        return ['July', 'August','September']
    elif period =="Q4":
        return ['October', 'November','December']
    elif period =="H1":
        return ['January', 'February','March','April', 'May','June']
    elif period =="H2":
        return ['July', 'August','September','October', 'November','December']
    elif period =="Annual":
        return ['January', 'February','March','April', 'May','June','July', 'August','September','October', 'November','December'] 
    else:
        return [period]

def get_period_as_int(period):
    if period =="Q1":
        return int(1)
    elif period =="Q2":
        return int(2)
    elif period =="Q3":
        return int(3)
    elif period =="Q4":
        return int(4)
    elif period =="H1":
        return int(1)
    elif period =="H2":
        return int(2)
    elif period =="Annual":
        return int(1)
def get_period(date1, date2):
    date_not_valid= ""
    Q=["Q1","Q2", "Q3", "Q4"]
    Half=["H1","H2"]		
    if date1 is None:
        date_not_valid = "Start date is not valid date"
    if date2 is None :
        if len(date_not_valid)>0:
            date_not_valid  = "Both Start and End dates are not valid dates"
        else :
            date_not_valid = "End date is not valid date"		


    if len(date_not_valid)>0:
        return date_not_valid
    if quarter(date1) == quarter(date2):
        return Q[quarter(date1)-1]
    elif half(date1) == half(date2):
        return Half[half(date1)-1]
    elif date1.year == date2.year:
        return "Annual"	
    else :
        return "Plans should be within a year"	

def quarter(date_instance):
	
	if date_instance.month in (1, 2, 3):
		return 1	
	elif date_instance.month in (4, 5, 6):
		return 2
	elif date_instance.month in (7, 8, 9):
		return 3
	elif date_instance.month in (10, 11, 12):
		return 4				

def half(date_instance):
    if date_instance.month in (1, 2, 3,4,5,6):
        return 1
    elif date_instance.month in (7, 8, 9,10, 11, 12):
        return 2



period_list= {"Annual":"Annual", "H1":"First Half", "H2":"Second Half" , 
	              "Q1":"First Quarter", "Q2": "Second Quarter", "Q3":"Third Quarter", "Q4":"Fourth Quarter"}


def month_from_int_to_string (month_int):
    if month_int ==1:
        return 'January'
    elif month_int ==2:
        return 'February'
    elif month_int ==3:
        return 'March'
    elif month_int ==4:
        return 'April'
    elif month_int ==5:
        return 'May'
    elif month_int ==6:
        return 'June'
    elif month_int ==7:
        return 'July'
    elif month_int ==8:
        return 'August'
    elif month_int ==9:
        return 'September'
    elif month_int ==10:
        return 'October'
    elif month_int ==11:
        return 'November'
    elif month_int ==12:
        return 'December'
    else:
        return "Not know Month"
        
def short_weekday_from_int_to_string(day_int):
    if day_int ==1:
        return 'mon'
    elif day_int ==2:
        return 'tues'
    elif day_int ==3:
        return 'wed'
    elif day_int ==4:
        return 'thur'
    elif day_int ==5:
        return 'frid'
    elif day_int ==6:
        return 'sat'
    elif day_int ==7:
        return 'sun'

def short_month_from_int_to_string (month_int):
    if month_int ==1:
        return 'jan'
    elif month_int ==2:
        return 'feb'
    elif month_int ==3:
        return 'mar'
    elif month_int ==4:
        return 'apr'
    elif month_int ==5:
        return 'may'
    elif month_int ==6:
        return 'jun'
    elif month_int ==7:
        return 'jul'
    elif month_int ==8:
        return 'aug'
    elif month_int ==9:
        return 'sept'
    elif month_int ==10:
        return 'oct'
    elif month_int ==11:
        return 'nov'
    elif month_int ==12:
        return 'dec'
    else:
        return "none"

def month_from_string_to_int (month_string):
    if month_string in ("Jan", "January"):
        return int(1)
    elif month_string in ("Feb", "February"):
        return int(2)
    elif month_string in ("Mar", "March"):
        return int(3)
    elif month_string in ("Apr", "April"):
        return int(4)
    elif month_string in ("May", "May"):
        return int(5)
    elif month_string in ("Jun", "June"):
        return int(6)
    elif month_string in ("Jul", "July"):
        return int(7)
    elif month_string in ("Aug", "August"):
        return int(8)
    elif month_string in ("Sep", "September"):
        return int(9)
    elif month_string in ("Oct", "October"):
        return int(10)
    elif month_string in ("Nov", "November"):
        return int(11)
    elif month_string in ("Dec", "December"):
        return int(12)

def get_current_user_groups(user):
    user_set=[]
    if user.groups.exists():
        user_set = list(user.groups.values_list('name',flat = True)) 
    return user_set

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

