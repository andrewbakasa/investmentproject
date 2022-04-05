import datetime
import pandas as pd

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



