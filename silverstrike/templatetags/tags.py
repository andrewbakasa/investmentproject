import math
from django import template

from trading.models import Investment, Investor
from django.db.models import Q


register = template.Library()


@register.simple_tag
def call_method(obj, method_name, *args):
    #print('method,,,,,name')
    #print(method_name)
    method = getattr(obj, method_name,)
    #print(method)
    return method(*args)

@register.simple_tag
def userIsOwnerAttrMethod(model, user):
    return model.userIsOwnerAttr(user)

@register.simple_tag
def userInvestorRejectedMethod(model, user):
    return model.userIsInvestorRejectedAttr(user)

@register.simple_tag
def userInvestorMethod(model, user):
    return model.userIsInvestorAttr(user)


@register.simple_tag
def userHasOrderProductMethod(model, product):
    if isinstance(model,dict) or isinstance(model,list):
        Found= False
        for i in model:
            if (str(i['product']['id']) == str(product.id)):
                Found= True
                break
        if Found == True:
            return "mycart"
        else:
            return "mycart_na"
    elif model ==None:
        return "mycart_na"
    return model.productIsInMyCart(product)


@register.simple_tag
def userInvestorValueMethod(model, user):
    return model.userInvestorValue(user)

@register.simple_tag
def userInvestorPercentMethod(model, user):
    return model.userInvestorPercent(user)



@register.simple_tag
def UserIsInvestorStatement(model, user):
    return model.userIsInvestorStatement(user)

@register.simple_tag
def UserIsInvestorStake(model, user):
    return model.userIsInvestorStake(user)



@register.simple_tag
def userhasNewInvestorsMethod(user):
    #All investors who are investing in investments i created 
    queryset = Investor.objects.filter(Q(investment__creater=user),Q(application_status='pending'))#
    if queryset.count() > 0 :     
        return 'mymessages'

    return 'mymessages_na'

@register.simple_tag
def useracceptedAsInvestorMethod(user):
    #All investments i have been accepted...
    #removes deleted investments 
    queryset = Investor.objects.filter(Q(user=user),Q(application_status='accepted'), Q(investment__isnull= False))#
    
    if queryset.count() > 0 :     
        return 'mymessages2'

    return 'mymessages2_na'


@register.simple_tag
def userInvestorEngagedMethod(model, user):
    is_investor, record= model.userIsInvestor_2(user)
    #print('.............')
    #print(is_investor, record)
    if is_investor:
        #print(record.application_status)
            #investor cannot be allowed to view blogs
        if record.application_status =='engagement':
            #print('inside......')
            return 'blogs'

    return 'blogs_na'

@register.simple_tag
def userNewInvestorsCountMethod(user):
    queryset = Investor.objects.filter(Q(investment__creater=user),Q(application_status='pending'))#
    #print(queryset,queryset.count()) 
    return queryset.count()


@register.simple_tag
def useracceptedInvestmentsCountMethod(user):
    queryset = Investor.objects.filter(Q(user=user),Q(application_status='accepted'))#
    #print(queryset,queryset.count()) 
    return queryset.count()

@register.filter
def negate(value):
    return -value


@register.filter
def intvalue(value):
    return int(value)

@register.filter
def shrink_num(value):
    """
    Shrinks number rounding
    123456  > 123,5K
    123579  > 123,6K
    1234567 > 1,2M
    """
    value =str(value)
    value2 = value.split('.')[0]
    #print(type(value2),value2,"isdigit", value2.isdigit(),len(value2.split('-'))>1 )
    #strip negative number
    # if len(value2.split('-'))>1:
    #     value2= value2#value.split('-')[1]

    if value2.isdigit() or len(value2.split('-'))>1:
        #print("digit", value)
        value_int = int(value2)
        if abs(value_int) >= 1000000000:
            value2 = "%.1f%s" % (value_int/1000000.00, 'B')
            return value2
        elif abs(value_int) >= 1000000:
            value2 = "%.1f%s" % (value_int/1000000.00, 'M')
            return value2
        else:
            if abs(value_int) >= 1000:
                value2 = "%.1f%s" % (value_int/1000.0, 'k')
                return value2
    return value
