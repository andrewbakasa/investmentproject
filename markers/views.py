"""Markers view."""

from distutils import errors
from http.client import HTTPResponse
from urllib import request
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import F

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
        user_tc_instance, tc_created = TradedCurrency.objects.get_or_create(created_by=self.request.user, complete=False)
        if tc_created:
            ul_instance, location_created = UserLocation.objects.get_or_create(user=request.user)
            if location_created:
                #save location Point
                ul_instance.location =user_location
                ul_instance.save()
            user_tc_instance.residence =ul_instance
            user_tc_instance.save()
        #user expectation
        uc_queryset = TradedCurrency.objects.filter(
                      Q(currency_offered=user_tc_instance.currency_expected),
                      Q(currency_expected=user_tc_instance.currency_offered)
                      ).annotate(distance=Distance('residence__location',  
                                            user_location)).order_by('distance')[0:6]
        serializer = TradedCurrencySerializer(uc_queryset, many=True)
      
        return Response(serializer.data, status=status.HTTP_200_OK)


""" 
    user = models.ForeignKey(User, null=True, blank=True, on_delete= models.SET_NULL)
    residence = models.ForeignKey(UserLocation,verbose_name="location", on_delete= models.SET_NULL,null=True, blank=False)
    currency_offered =models.ForeignKey(Currency, on_delete= models.SET_NULL, null=True)
    currency_expected = models.ForeignKey(Currency, on_delete= models.SET_NULL, null=True)
    rate_expected = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    value = models.IntegerField()
    complete =models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL,null=True)
"""

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
        product_queryset = Product.objects.filter(Q(description__icontains =slug)).annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
  
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
        user_tc_instance, tc_created = TradedCurrency.objects.get_or_create(created_by =self.request.user, complete=False)
        if tc_created:
            ul_instance, location_created = UserLocation.objects.get_or_create(user=request.user)
            if location_created:
                #save location Point
                ul_instance.location =user_location
                ul_instance.save()
            user_tc_instance.residence =ul_instance
            user_tc_instance.save()

        #Q(description__icontains =slug)
        # Q(value =slug)
        # Q(expected =slug)
        # Q(offered =slug)
        #user expectation
        uc_queryset = TradedCurrency.objects.filter(
                      Q(currency_offered=user_qs.currency_expected),
                      Q(currency_expected=user_qs.currency_offered)
                      ).annotate(distance=Distance('residence__location',  
                                            user_location)).order_by('distance')[0:6]
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
        #print('Location >>>>>>>>>>>........', item.location, item.location.x, item.location.y)
        form = self.form_class(instance= item,  initial={'lng': item.location.x, 'lat': item.location.y})
        #print(form)
        # form.lng =item.location.x
        # form.lat =item.location.y
        context={}
        context["form"] = form
        context["edit"] = True
        context["x"] = item.location.x
        context["y"] = item.location.y
        return render(request, self.template_name, context)
    
   
    def form_valid(self, form):
        print('>>>>>>>', self.request.POST["lat"], self.request.POST["lng"])
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

    instance, created = UserLocation.objects.get_or_create(user=request.user)

    location = Point(float(lng), float(lat),srid=4326)
    instance.location = location

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

        user_tc_instance, tc_created = TradedCurrency.objects.get_or_create(created_by =self.request.user, complete=False)
        if tc_created:
            ul_instance, location_created = UserLocation.objects.get_or_create(user=request.user)
            if location_created:
                #save location Point
                ul_instance.location =user_location
                ul_instance.save()
            user_tc_instance.residence =ul_instance
            user_tc_instance.save()
        #context["form"] =TradedCurrencyForm(initial ={'created_by': self.request.user})
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
		#first time call from loco failure list
        # kwargs = super().get_form_kwargs()
        # kwargs.update({'user': self.request.user})
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
            ul_instance, location_created = UserLocation.objects.get_or_create(user=request.user)
            if location_created:
                #save defaul location Point
                ul_instance.location =user_location
                ul_instance.save()
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
