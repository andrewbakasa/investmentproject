"""Markers view."""

from distutils import errors
from http.client import HTTPResponse
import math
from urllib import request
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import F , Case, CharField, Value, When
from django.db.models.functions import Abs
import json

from django.core.serializers import serialize
from django.views.generic.base import TemplateView
from common.decorators import allowed_users, login_in_user_only_with_routing
from customers.forms import ProductForm

from markers.forms import MarkerForm, ShopForm, TradedCurrencyForm, TradedCurrencyFormUpdate
from store.models import Product, Shop

from .models import Marker, TradedCurrency, UserLocation
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render,redirect

from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.utils.decorators import method_decorator


from django.urls import reverse, reverse_lazy
from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework_gis import filters


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

   
# ----our clients dont pass here but leapfrog to their page
#import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

from django.db.models import Q, F, ExpressionWrapper, IntegerField
from django.db.models import Max, Value, Min
from django.db.models.functions import Cast, Coalesce
from django.db.models import FloatField 


longitude= 32.658821726608004#27.553711
latitude =-18.985227330788064#-20.756114
# Point(Lat,Long)
user_location = Point(longitude,latitude,srid=4326)

from django.contrib.gis.serializers.geojson import Serializer 

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry,Point
from rest_framework.decorators import action
from django_filters import rest_framework  as filters
#from .filter import ProductFilter
from .models import  Marker
from store.models import Product

from . serializers import  ProductSerializer, TradedCurrencySerializer

# Normally in views.py
class MapView(TemplateView):
    model = Shop
    form_class = ShopForm
    template_name = 'markers/create.html'

    def get(self, request, *args, **kwargs):        
        context={}       
        context["form"] = self.form_class        
        return render(request, self.template_name, context)
       
class MapViewCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Shop
    template_name = 'markers/create.html'
    success_url = reverse_lazy('user_products')

    def get_form_class(self):
        return ShopForm

   
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        form = ShopForm(request.POST) # class based view.
        if form.is_valid():
            # for f in files:
            #     ...  # Do something with each file.
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

class AjaxableResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        print(context)
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response

class MapUpdateView(LoginRequiredMixin, AjaxableResponseMixin, generic.edit.UpdateView):
    #template_name = 'customers/product_edit.html'
    template_name = 'customers/product_edit_modal.html'
    #template_name = 'customers/products.html'
    model = Product
    success_url = reverse_lazy('products')

    form_class= ShopForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # assign the object to the view
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        
        pk = kwargs.get('pk', None)
        shop = get_object_or_404(Shop, pk=pk)
        form = ShopForm(request.POST or None, request.FILES or None,instance=shop) # class based view.
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return generic.edit.ProcessFormView.get(self, request, *args, **kwargs)
    
class  MapUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    form_class= ShopForm
    model = Product
    template_name = 'customers/product_edit_modal.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # assign the object to the view
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        
        pk = kwargs.get('pk', None)
        product = get_object_or_404(Shop, pk=pk)
       
        form = ShopForm(request.POST or None, request.FILES or None, instance=product) # class based view.
        #print(form)
        data =  dict()
        errors= None
   
       
        
        if form.is_valid():
            product= form.save()

            product_item_object =model_to_dict(product)
            product_item_object['image']=str(product_item_object['image'])
            categories=""
           
            for x in product_item_object['categories']:
                categories = categories +   str(x.name) + ', '  
            product_item_object['categories']=  categories[:len(categories)-2]
          
            
            companies=""
            for x in product_item_object['company']:
                companies  = companies + str(x.name)  
            product_item_object['company']=  companies
            

            data['product'] = product_item_object
        else:
            errors=form.errors
            data['error'] = errors
        return JsonResponse(data)
   
  
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    #filterset_class = ProductFilter
    filter_backends = [filters.DjangoFilterBackend]
   
    @action(detail=False, methods=['get'])
    def get_nearest_facilities(self, request):
        x_coords = request.GET.get('x', None)
        y_coords = request.GET.get('y', None)
        if x_coords and y_coords:
            user_location = Point(float(x_coords), float(y_coords),srid=4326)
            nearest_five_facilities = Product.objects.annotate(distance=Distance('location',user_location)).order_by('distance')[:5]
            serializer = self.get_serializer_class()
            serialized = serializer(nearest_five_facilities, many = True)
            print(nearest_five_facilities)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class ProductLocationView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 3. Retrieve
    def get(self, request,  *args, **kwargs):
       #----------------------------------
       
        x =  self.kwargs.get('x')
        y =  self.kwargs.get('y')
        user_location = Point(float(x), float(y),srid=4326)
        product_queryset = Product.objects.annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
        serializer = ProductSerializer(product_queryset, many=True)
      
        return Response(serializer.data, status=status.HTTP_200_OK)
""" 
A: DATA-MATRIX

Client     Expected_Amt   Offered  Difference  Diff      Rate_Offered  Rate_Expected Rate_Diff   RD      Distance
1            300          400      |300-400|   g2*100       700           650        |700-650|  g2*50    5km
2            300          100      |300-100|   g1*200       750           650        |750-650|  g2*100  .5km
3            300          200      |300-200|   g2*100       600           650        |600-650|  g1*50   .1km


B: COST PENALTY

                           ^
             * g2          |                         
              *            |
               *           |
                *          |
                 *         |
                 +*------->|                                       ^ g1
                 + *       |                                 ^
                 +  *      |                            ^
                 +   *     |                       ^
                 +    *    |                 ^
                 +     *   |<-----------+^
                 +      *  |        ^   +                               g1 <g2
                 +       * |    ^       +
_________________+_________*^___________+__________________________________________                           
(-) NEGATIVE    -1                      +1                            (+) POSITIVE

Cost Fn = a*Rate_Diff + b*Amt_Diff + Distance
        =a* {g1*R || g2*R} + b* {g1*A || g2*A} + D
normalise
        A*[0-1]   +  B*[0-1]  +   C*[0-1]  
        A=B=C => #33.3% each 

        max <---> min of population  

C: Available CASH VS DEMAND









"""
class CurrencyLocationView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 3. Retrieve
    def get(self, request,  *args, **kwargs):
       #----------------------------------
       
        x =  self.kwargs.get('x')
        y =  self.kwargs.get('y')
        update_user_location(self.request,x,y)
        user_location = Point(float(x), float(y),srid=4326)
        # user allowed one incomplete record only
        user_tc_instance=get_and_save_instance(self.request.user, user_location)
        #user expectation
        dict_=get_aggregate(user_tc_instance)       
        uc_queryset= get_queryset(user_tc_instance,dict_)   
        # panda here
        serializer = TradedCurrencySerializer(uc_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def get_and_save_instance(user, user_loc):
    user_tc_instance, tc_created = TradedCurrency.objects.get_or_create(created_by=user, complete=False)
    if tc_created:
        qs= UserLocation.objects.filter(user=user)
        ul_instance=None
        if qs:
            ul_instance= qs.first()
            ul_instance.location =user_loc
            ul_instance.save()
        else:
            ul_instance =UserLocation.objects.create(user=user, location =user_loc)
            ul_instance.save()
        
        user_tc_instance.residence =ul_instance
        user_tc_instance.save()
    else:
        if  user_tc_instance.residence:
            #update residence
            user_tc_instance.residence.location =user_loc
            user_tc_instance.save()
        else :
            # no residence
            qs= UserLocation.objects.filter(user=user)
            ul_instance=None
            if qs:
                ul_instance= qs.first()
                ul_instance.location =user_loc
                ul_instance.save()
            else:
                ul_instance =UserLocation.objects.create(user=user, location =user_loc)
                ul_instance.save()
            # save residences
            user_tc_instance.residence =ul_instance
            user_tc_instance.save()
    return  user_tc_instance    
def get_aggregate(user_tc_instance):
    total_agg = TradedCurrency.objects.filter(
        Q(complete=False),
        Q(currency_offered=user_tc_instance.currency_expected),
        Q(currency_expected=user_tc_instance.currency_offered)
        ).aggregate(
            value_range=Max('value', output_field=FloatField()) - Min('value'),
            value_min= Min('value'),
            rate_expected_range=Max('rate_expected', output_field=FloatField()) - Min('rate_expected'),
            rate_expected_min= Min('rate_expected'),
            distance_range=Max(
                                Distance(
                                    'residence__location',  
                                        user_location
                                    )
                                ) 
                            - 
                            Min(
                                Distance(
                                'residence__location',  
                                    user_location
                                )
                            ),
            distance_min= Min(
                                Distance(
                                    'residence__location',  
                                        user_location
                                    ),
                        )
                            
    ) 
    dict_ = {}
    dict_['value_range']=total_agg['value_range'] if not total_agg['value_range']== 0 else 1
    #value_min=total_agg['value_min'] 
    dict_['rate_expected_range']=total_agg['rate_expected_range'] if not total_agg['rate_expected_range']== 0 else 1
    dict_['rate_expected_min']=total_agg['rate_expected_min'] 
    dict_['distance_range']=total_agg['distance_range'].m if not total_agg['distance_range'].m== 0 else 1
    dict_['distance_min']=total_agg['distance_min'].m
    return dict_   

def get_queryset(user_tc_instance,dict_):
    #A*[0-1]   +  B*[0-1]  +   C*[0-1] 
    A = 0.3 #available cash
    B = 0.2 # rate wanted
    C = 0.5 # distance
    g1= 1 # higher penalty for non -compliance
    g2= 0.5 #over and above less gradient
    uc_queryset = TradedCurrency.objects.filter(
                    Q(complete=False),
                    Q(currency_offered=user_tc_instance.currency_expected),
                    Q(currency_expected=user_tc_instance.currency_offered)
                    ).annotate(
                        amt_compliant=Case(
                                When(value__lt=user_tc_instance.value, then=(g1*Abs(F('value')- user_tc_instance.value))/dict_['value_range']),
                                When(value__gt=user_tc_instance.value, then=(g2*Abs(F('value')- user_tc_instance.value))/dict_['value_range']),
                                default=Value(0),
                                output_field=FloatField(),
                        )
                    ).annotate(
                        rank=ExpressionWrapper(
                                A*F('amt_compliant') +
                                Abs(B*(F('rate_expected')- dict_['rate_expected_min'])/dict_['rate_expected_range']) +
                                Abs(C*(Distance('residence__location',  user_location)- dict_['distance_min'])/dict_['distance_range']),
                                output_field=FloatField()
                            ),
                        distance=Distance(
                                'residence__location',  
                                user_location
                            ),
                    ).order_by('rank')[0:6]  
    return uc_queryset
@method_decorator(login_in_user_only_with_routing(), name='dispatch')   
class ProductLocationSlugView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 3. Retrieve
    def get(self, request,  *args, **kwargs):
        slug =  self.kwargs.get('slug')
        x =  self.kwargs.get('x')
        y =  self.kwargs.get('y')
        #print('My viewpoint:', x,y)
        user_location = Point(float(x), float(y),srid=4326)

        total_agg = Product.objects.filter(Q(description__icontains =slug)).aggregate(
                    price_range=Max('price')- Min('price'),
                    price_min= Min('price'),
                    distance_range=Max(
                                        Distance(
                                            'shop__location',  
                                                user_location
                                            )
                                        ) 
                                    - 
                                    Min(
                                        Distance(
                                        'shop__location',  
                                            user_location
                                        )
                                    ),
                    distance_min= Min(
                                        Distance(
                                            'shop__location',  
                                                user_location
                                            ),
                                )
                                
                    ) 
        dict_ = {}
        dict_['price_range']=total_agg['price_range'] if not total_agg['price_range']== 0 else 1
        dict_['price_min']=total_agg['price_min'] 
        dict_['distance_range']=total_agg['distance_range'].m if not total_agg['distance_range'].m== 0 else 1
        dict_['distance_min']=total_agg['distance_min'].m
    
        A= 0.25 #price factor
        B= 0.75 #distance factor
        product_queryset = Product.objects.filter(Q(description__icontains =slug)).annotate(
                        rank=ExpressionWrapper(
                                Abs(A*(F('price')- dict_['price_min'])/dict_['price_range']) +
                                Abs(B*(Distance('shop__location',  user_location)- dict_['distance_min'])/dict_['distance_range']),
                                output_field=FloatField()
                            ),
                        distance=Distance(
                                'shop__location',  
                                user_location
                            ),
                    ).order_by('rank')[0:6]
  
        serializer = ProductSerializer(product_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(login_in_user_only_with_routing(), name='dispatch')   
class TradedCurrencyLocationSlugView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 3. Retrieve
    def get(self, request,  *args, **kwargs):
        slug =  self.kwargs.get('slug')
        x =  self.kwargs.get('x')
        y =  self.kwargs.get('y')
        update_user_location(self.request,x,y)
        user_location = Point(float(x), float(y),srid=4326)
        # user allowed one incomplete record only
        user_tc_instance=get_and_save_instance(self.request.user, user_location)
       
        #user expectation
        dict_=get_aggregate(user_tc_instance)       
        uc_queryset= get_queryset(user_tc_instance,dict_) 

        serializer = TradedCurrencySerializer(uc_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class AddProduct():
    pass
def add_shop(request, *args, **kwargs):
    if request.method == "POST":
        form= ShopForm(request.POST)
        lat, lng = request.POST["lat"], request.POST["lng"]
        #print(lat, lng)
        if form.is_valid():
            location = Point(float(lng), float(lat),srid=4326)
            instance = form.save(commit=False)
            instance.location = location
            instance.user = request.user
            instance.save()
        else:
            print(form.errors)
           
    form= ShopForm()
    context = {
        "form":form,
        "json_user_location_x": user_location.x,
        "json_user_location_y": user_location.y
    }
    return render(request,'markers/addshop.html',context)

class ShopUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Shop
    template_name = 'markers/addshop.html'
    form_class = ShopForm

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Shop,pk=self.kwargs.get('pk'))
        form = self.form_class(instance= item,  initial={'lng': item.location.x, 'lat': item.location.y})
        context={}
        context["form"] = form
        context["edit"] = True
        context["x"] = item.location.x
        context["y"] = item.location.y
        return render(request, self.template_name, context)
    
   
    def form_valid(self, form):
        #print('>>>>>>>', self.request.POST["lat"], self.request.POST["lng"])
        lat, lng = self.request.POST["lat"], self.request.POST["lng"]
        instance = form.save(commit=False)
        location = Point(float(lng), float(lat),srid=4326)
        instance.location = location
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        return redirect('user_shops')
  
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
def update_user_location(request,lng,lat):
    location = Point(float(lng), float(lat),srid=4326)
    #instance, created = UserLocation.objects.get_or_create(user=request.user)
    qs= UserLocation.objects.filter(user=request.user)
    if qs:
        instance= qs.first()
        instance.location = location
        instance.save()
    else:
        instance =UserLocation.objects.create(user=request.user, location =location)
        instance.save()
    
    
def edit_shop(request, *args, **kwargs):
    if request.method == "POST":
        form= ShopForm(request.POST)
        lat, lng = request.POST["lat"], request.POST["lng"]
        #print(lat, lng)
        if form.is_valid():
            location = Point(float(lng), float(lat),srid=4326)
            instance = form.save(commit=False)
            instance.location = location
            instance.user = request.user
            instance.save()
        else:
            print(form.errors)
           
    form= ShopForm()
    context = {
        "form":form,
        "json_user_location_x": user_location.x,
        "json_user_location_y": user_location.y
    }
    return render(request,'markers/addshop.html',context)
class CurrencyTradingLocationViewLandingPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'markers/currencytrading.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      

        longitude= 32.658821726608004#27.553711
        latitude =-18.985227330788064#-20.756114
        
        # Point(Lat,Long)
        user_location = Point(longitude,latitude,srid=4326)

        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
        
        x = user_location.x# default val
        y =  user_location.x# default val
        user_location = Point(float(x), float(y),srid=4326)#default

        user_tc_instance=get_and_save_instance(self.request.user, user_location)
        context["form"] =TradedCurrencyForm(instance =user_tc_instance)
        return context

class ProductLocationViewLandingPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'markers/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      

        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
    
        return context


def userlocation_data(request):
   
    cookie_data = cookie_userlocation(request)
    print('row data:', cookie_data)
    if cookie_data:
        if 'latLng' in cookie_data :
            print(cookie_data['latLng'], type(cookie_data['latLng']))
            if isinstance(cookie_data['latLng'],list):
                latitude = cookie_data['latLng'][0]
                longitude = cookie_data['latLng'][1]

                return {
                    'lng': longitude,
                    'lat': latitude,
                }
    return {}

# create cart for guest user
def cookie_userlocation(request):
    try:
        userlocation = json.loads(request.COOKIES['userlocation'])
    except:
        userlocation = {}

    return {
        'latLng': userlocation,
    }

login_required(login_url="account_login")
def create_tc_ajax(request):
	if request.method == 'POST':
		form = TradedCurrencyForm(request.POST or None)
	else:
		
		form = TradedCurrencyForm(initial={'created_by': request.user })
	return create_tc(request,form,'markers/tradedcurrency_modal.html')


login_required(login_url="account_login")
def create_tc(request,form,template_name):

    data = dict()
    errors= None
    if request.method == 'POST':
        errors=form.errors
        
        if form.is_valid():
            form.save()
            #form.us
            data['form_is_valid'] = True
            latest = TradedCurrency.objects.latest('id').id
            record = TradedCurrency.objects.get(pk=latest)
            item_object = model_to_dict(record)
            print(item_object)
           
          
            data['model'] = item_object
        else:
            data['form_is_valid'] = False
            # print('nofield errors: ',form.non_field_errors)
            # print('errors:::',form.errors)
    context = {
        'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    data['error']=errors
    return JsonResponse(data)

login_required(login_url="account_login")
def tc_update(request):
   
    #first time creation giving Error 500 on Heroku 23 Sep 2022
    instance_,tc_created = TradedCurrency.objects.get_or_create(created_by=request.user, complete=False)
    if tc_created:
            qs= UserLocation.objects.filter(user=request.user)
            ul_instance=None
            if qs:
                ul_instance= qs.first()
                ul_instance.location =user_location
                ul_instance.save()
            else:
                ul_instance =UserLocation.objects.create(user=request.user, location =user_location)
                ul_instance.save()

          
            instance_.residence =ul_instance
            instance_.save()
    else:
        if  not instance_.residence:
            # no residence create new or attache Userlocatio
            qs= UserLocation.objects.filter(user=request.user)
            ul_instance=None
            if qs:
                ul_instance= qs.first()
                ul_instance.location =user_location
                ul_instance.save()
            else:
                ul_instance =UserLocation.objects.create(user=request.user, location =user_location)
                ul_instance.save()
            # save residences
            instance_.residence =ul_instance
            instance_.save()
    if request.method == 'POST':
        form = TradedCurrencyFormUpdate(request.POST or None, instance=instance_)
    else:
        form = TradedCurrencyFormUpdate(instance=instance_)
    return save_all_tc(request,form,'markers/tc_edit_modal.html')

def save_all_tc(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            #print(form.instance.id)
            data['form_is_valid'] = True
            
            # retrieve product
            pk = form.instance.id
            obj = get_object_or_404(TradedCurrency,pk=pk)
            item_object = model_to_dict(obj)
            
            data['product'] = item_object
        else:
            data['form_is_valid'] = False
            data['error']= form.errors
    context = {
    'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    #print(data)
    return JsonResponse(data)
