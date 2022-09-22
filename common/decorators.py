from django.http import HttpResponse
from django.shortcuts import redirect

# for FBV
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


# for CBV & FBV
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = None
            if request.user.groups.exists():
                groups = request.user.groups.values_list('name', flat=True)
            for group in groups:
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator

# for FBV
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            groups = request.user.groups.all()
            for gr in groups:
                if gr.name == 'admin':
                    return view_func(request, *args, **kwargs)           
            return redirect('home_page')
        else:
            return redirect('home_page')
    
    return wrapper_func
# for CBV & FBV
def registered_user_only_with_client_routing():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            groups = None
            if request.user.groups.exists():
                groups = request.user.groups.all()
                group = groups[0].name
            if group  == 'customer' or group  == 'visitor':
                #some users has customer role with other role like admin
                if len(groups)==1 :
                    return redirect('home_page')
                elif len(groups)==2:
                    if groups[0].name in ['visitor', 'customer'] and groups[1].name in ['visitor', 'customer']:
                        return redirect('home_page')
                    else:
                        return view_func(request, *args, **kwargs)
                else:
                    return view_func(request, *args, **kwargs)

            elif group != None:# any other role allowed
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def login_in_user_only_with_routing():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            #print(">>>>>>>>>>>>>>><><><><<><><><")
            if not request.user.is_authenticated:
               # print(",,,,,,,,,,,,,,,,,,,,, Logn please")
                #return HttpResponse("You are not authorized to view this page")
                return redirect('home_page')
                
               
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator