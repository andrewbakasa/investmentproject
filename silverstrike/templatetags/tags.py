from django import template


register = template.Library()


@register.simple_tag
def call_method(obj, method_name, *args):
    print('method,,,,,name')
    print(method_name)
    method = getattr(obj, method_name,)
    print(method)
    return method(*args)

@register.simple_tag
def userInvestorMethod(model, user):
    return model.userIsInvestorAttr(user)

@register.filter
def negate(value):
    return -value


@register.filter
def intvalue(value):
    return int(value)
