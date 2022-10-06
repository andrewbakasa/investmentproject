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

from .models import CurrencyTag, Marker, NearbyDistance, TradedCurrency, UserLocation
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


longitude =27.553711#32.658821726608004#
latitude  =-20.756114#=-18.985227330788064
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
        #print(context)
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
            #print(nearest_five_facilities)
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
        adj =  self.kwargs.get('adj') 
        update_user_location(self.request,x,y)
        user_location = Point(float(x), float(y),srid=4326)      
        # user allowed one incomplete record only
        user_tc_instance=get_and_save_instance(self.request.user, user_location)
        
        #user expectation
        dict_=get_aggregate(user_tc_instance, user_location)       
        uc_queryset= get_queryset(user_tc_instance,dict_, user_location,int(adj))   
        # panda here
        serializer = TradedCurrencySerializer(uc_queryset, many=True)
        match_partner= get_matching_partern_exist(serializer.data)
        
          
        # for  i  in serializer:
        #     print('this22....', i)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_matching_partern_exist(s_dict):
    for key, value in s_dict.items():
        if isinstance(value, list):
            for i in value:
                for key2, value2 in i.items():
                    if isinstance(value2, dict):
                        if key2=='properties':
                            #print(value2)
                            return value2['matching_partner']
    return False
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
        # Error not update user location check now
        if  user_tc_instance.residence:
            user_tc_instance.residence.location=user_loc# =ul_instance
            user_tc_instance.save()
            print('Location updated>>>', user_tc_instance.residence,)
        else:
            user_tc_instance.residence=ul_instance
            user_tc_instance.save()
    else:
        if  user_tc_instance.residence:
            #update residence,,,, is it updating?
            print("Updating location", user_loc)
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
def get_aggregate(user_tc_instance, user_location):
    
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
    #print('distance_range', dict_['distance_range'])
    if 'distance_range' in dict_:
        dict_['distance_range']=total_agg['distance_range'].m if not total_agg['distance_range'].m== 0 else 1
    else:
        dict_['distance_range']=1
    if 'distance_min' in dict_:
        dict_['distance_min']=total_agg['distance_min'].m
    else:
       dict_['distance_min']=1 
    return dict_   

def get_queryset(user_tc_instance,dict_, user_location, delta_adj):
    
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
                    ).order_by('rank')[0:6+int(delta_adj)]  

    # for i in uc_queryset:
    #     print(i.currency_offered,",", i.currency_expected,",",i.created_by,",",i.value)
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
        if 'distance_range' in dict_:
            dict_['distance_range']=total_agg['distance_range'].m if not total_agg['distance_range'].m== 0 else 1
        else:
            dict_['distance_range']=1
        if 'distance_min' in dict_:
            dict_['distance_min']=total_agg['distance_min'].m
        else:
            dict_['distance_min']=1 
    
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
        adj =  self.kwargs.get('adj') 
        update_user_location(self.request,x,y)
        user_location = Point(float(x), float(y),srid=4326)
        # user allowed one incomplete record only
        user_tc_instance=get_and_save_instance(self.request.user, user_location)
        
        #user expectation
        dict_=get_aggregate(user_tc_instance, user_location)       
        uc_queryset= get_queryset(user_tc_instance,dict_, user_location,int(adj)) 

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
        print('location updated......')
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
        context["user_name"] =self.request.user.username
        
        x = user_location.x# default val
        y =  user_location.x# default val
        
     

        user_location = Point(float(x), float(y),srid=4326)#default

        user_tc_instance=get_and_save_instance(self.request.user, user_location)
        context["form"] =TradedCurrencyForm(instance =user_tc_instance)
        # dummy_change_location(self.request)
        return context

def dummy_change_location(request):
    x= 32.658821726608004#27.553711
    y =-20.985227330788064#-20.756114
    user_location = Point(float(x), float(y),srid=4326)#default
    user_tc_instance, tc_created = TradedCurrency.objects.get_or_create(created_by=request.user, complete=False)   
    user_tc_instance.residence.location =user_location   
    user_tc_instance.save() 
class ProductLocationViewLandingPage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'markers/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      

        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
    
        return context


def userlocation_data(request):
   
    cookie_data = cookie_userlocation(request)
    #print('row data:', cookie_data)
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


# class CurrencyTag(models.Model):
# target = models.ForeignKey(TradedCurrency,related_name="targetA", on_delete= models.SET_NULL, null=True)
# source = models.ForeignKey(TradedCurrency,related_name="sourceA", on_delete= models.SET_NULL, null=True)
# date_created = models.DateTimeField(auto_now_add=True, null=True)
# last_modified=models.DateTimeField(auto_now=True)
# created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
# def __str__(self):
   
   
""" 
 Source (A)                  Target (Mark)                 Other user (B)   
 /\                      -----                          /\
/Ua\  ------->          |_u1__|  <-----------||--------/ub\  qs_other_users  . Check target of other user
    \
      \  
        \
          ||
            \  
              \  
         \       \       ----- 
          \         \   |_u2__|

             \
              ||
                \
                
                  \

                     \
                       \ ------
                        |_u3__|

"""
def distance_to_target(target_id, request):
    user_location=TradedCurrency.objects.filter(
                   Q(created_by=request.user), Q(complete=False)
            ).first().residence.location
    target= TradedCurrency.objects.filter(
                    pk=target_id).annotate(
                        distance=Distance('residence__location',user_location)
            ).first()
    return target.distance.m
def create_user_currency_tag_ajax(request, target_id,  *args, **kwargs):
    data={}	
    if request.method == 'POST':
        if request.is_ajax():
            # incoming A
            target= TradedCurrency.objects.filter(pk=target_id).first()
            #i am stading here
            """ Source is keeping changing........B """
            source=TradedCurrency.objects.filter(Q(created_by=request.user), Q(complete=False)).first()#,tc_created = TradedCurrency.objects.get_or_create(created_by=request.user, complete=False)
           
           #does the user have ACTIVE tag going to target?EXCLUDED SATIFIED TAGS
            qs= CurrencyTag.objects.filter(Q(target =target),Q(source =source), Q(created_by=request.user), Q(target__complete=False))#
            if qs:
                #if Toggle/add/remove
                data['Found tags created me:Reseting'] ='Yes'
                CurrencyTag.objects.filter(Q(target =target), Q(source=source), Q(created_by=request.user), Q(target__complete=False)).delete()
               
            else:
                #check if any user is tracking this person: 
                """ OTHER SUITORS MAYBE TRACKING
                SURVIVAL OF THE FITTEST
                CHECK IF NO MATCH YES THEN MATCH
                """
                data['No tags found:'] ='Yes'
                # other users tracking and matching ACTIVE
                qs_other_users =CurrencyTag.objects.filter(Q(target =target), Q(target__complete=False))#.exclude(created_by=request.user)

                matching_found= False
                for i in qs_other_users:
                    #print('Chech partner availabilty')
                    if i.matching_partner():
                        #print('Found a parnter')
                        data['Found a matching partner'] ='Yes'
                        matching_found=True
                        break

                if not matching_found:
                    data['No matching Found'] ='yes'
                    # delete all tags  created by me with source
                    CurrencyTag.objects.filter(Q(target =target), Q(source =source), Q(created_by=request.user),Q(target__complete=False)).delete()
                    #print('Creating a Maching here')
                    instance = CurrencyTag.objects.create(target =target, source =source, created_by=request.user)
                    instance.save() 
                    data['New Tags created'] ='Yes'
                else:
                    pass
                    #nothing already
                    #print('Matching found, Polygamy disallowed.......')
                    #you cant tag alreay matched parten
                    data['Polygamy disallowed'] ='Yes'
                    #CurrencyTag.objects.filter(Q(target =target),Q(source =source), Q(created_by=request.user)).delete()
           
           
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})


def complete_currency_ajax(request, target_id,  *args, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            # incoming A : CLOSE
            target= TradedCurrency.objects.filter(pk=target_id).first()
            target.complete= True           
            target.save() 
            """ NOTIFY OWNER OF THIS CHANGE....  """
            #i am stading here
            """ Source is keeping changing........B """ #AND TIS ALSO CLOSE
            source=TradedCurrency.objects.filter(Q(created_by=request.user), Q(complete=False)).first()#,tc_created = TradedCurrency.objects.get_or_create(created_by=request.user, complete=False)
            print('Saved!!!!!!!!!!!!!!!!!!!')
            source.complete= True           
            source.save() 
               
            data={}	
            item_object = {}
           
            return JsonResponse({"data":data})
        else:
            return JsonResponse({'error': True, 'data': 'errors'})  
        
    else:
        return JsonResponse({'error': True, 'data': "Request not ajax"})

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
            #print(item_object)
           
          
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


def update_nearby_user_ajax(request): 
    data = {}
    
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        #print('uid', uid)
        distance = request.POST.get('distance', None)
        qs= TradedCurrency.objects.filter(pk=uid)
        if qs:
            tdc= TradedCurrency.objects.filter(pk=uid).first()
            obj, created = NearbyDistance.objects.get_or_create(source=tdc)
            data = model_to_dict(tdc)
            if created:
                obj.distance =int(distance)
                obj.save()
                data['created'] ='New'
            else:
                # update distance onif it closer
                data['Updating'] ='Yes'
                if int(distance) < obj.distance:
                    obj.distance =int(distance)
                    obj.save()
                    data['Moved closer'] ='Yes'

   
    
    return JsonResponse({"data":data})

def remove_closed_deal_by_nearby_dist(target_id):
    source= TradedCurrency.objects.filter(pk=target_id).first()
            
    qs= NearbyDistance.objects.filter(Q(source =source)).first()
    if qs.distance <= 10:
        target= TradedCurrency.objects.filter(pk=target_id).first()
        target.complete= True           
        target.save() 


def update_all_deal_closed():
    #filter nearby distances.......................         
    qs= NearbyDistance.objects.filter(Q(distance__lte =10))
    for i in qs:
        source= i.source
        target =i.target

        source.complete= True           
        source.save() 
        target.complete= True           
        target.save() 

