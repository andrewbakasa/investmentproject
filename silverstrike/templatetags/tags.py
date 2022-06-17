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
def userInvestorMethod(model, user):
    return model.userIsInvestorAttr(user)

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
    #print(queryset,queryset.count()) 
    if queryset.count() > 0 :     
        return 'mymessages'

    return 'mymessages_na'

@register.simple_tag
def userNewInvestorsCountMethod(user):
    queryset = Investor.objects.filter(Q(investment__creater=user),Q(application_status='pending'))#
    #print(queryset,queryset.count()) 
    return queryset.count()

@register.filter
def negate(value):
    return -value


@register.filter
def intvalue(value):
    return int(value)
