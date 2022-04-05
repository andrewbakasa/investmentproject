import datetime


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def short_month_name(item):
    month_list = ['Jan', "Feb", "Mar", "Apr", "May", "Jun", "Jul" , "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    if int(item)> 0 and int(item) <= len(month_list):
        return month_list[int(item)-1]
    return item
