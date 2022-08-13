from django import template


register = template.Library()


@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url ='?{}={}'.format(field_name,value)

    if urlencode:
        querystring = urlencode.split('&')
        # main url : page=2&name=&gender=Feamle&age=8
        # querstring= ['page=2', 'name=' , 'gender=Femal', 'age=8']
        filtered_querystring =filter(lambda p:p.split('=')[0]!=field_name, querystring)
        encoded_querystring ='&'.join(filtered_querystring)
        url ="{}&{}".format(url,encoded_querystring)
        # url ={?page=2} & {name=& gender=Female&age=8}
    return url

