from django import template


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
def UserIsInvestorStatement(model, user):
    return model.userIsInvestorStatement(user)

@register.simple_tag
def UserIsInvestorStake(model, user):
    return model.userIsInvestorStake(user)


@register.filter
def negate(value):
    return -value


@register.filter
def intvalue(value):
    return int(value)
