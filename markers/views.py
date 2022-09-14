"""Markers view."""

from http.client import HTTPResponse

from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import F

import json

from django.core.serializers import serialize
from django.views.generic.base import TemplateView
from common.decorators import allowed_users, login_in_user_only_with_routing
from customers.forms import ProductForm

from markers.forms import MarkerForm, ShopForm
from store.models import Product, Shop

from .models import Marker
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render

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



latitude =-18.985227330788064#-20.756114
longitude= 32.658821726608004#27.553711
# Point(Lat,Long)
user_location = Point(longitude,latitude,srid=4326)

# def update_user_location (request):
#     userloc = userlocation_data(request)
#     print('my current loc: x:y', userloc)
#     if 'lat' in userloc and 'lng' in userloc :
#         user_location.x= userloc['lng']
#         user_location.y =userloc['lat']
#         print('FOUND IT EUREKA.........................updating user location>>>>>>>>>>>>>>>>')
  

# pnt = Point(5, 23)
# Note "X and Y coordinates". X is longitude, Y is latitude. In this example 5 is longitude and 23 is latitude.
# def park_insert(request):
#     form = ParkForm()
#     return render(request, 'addpark.html', {'form': form})
class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "markers/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        #----------------------------------
       
        queryset = Marker.objects.annotate(distance=Distance('location',  
                                                   user_location)).order_by('distance')[0:6]


        context["markers"] = json.loads(serialize("geojson", queryset))
        #----------------------------FOR TESTING::::::::-------
        #--------------------------------------------------
        queryset = Product.objects.annotate(shopname=F('shop__name'),location=F('shop__location')).annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
          
           
        context["markers"] = json.loads(serialize("geojson", queryset, fields=('name','location', 'distance'))) 
        #----------------------------------------------------
        #--------------------------------------------------
       
        dict_={}
        dict_['x']=user_location.x# long
        dict_['y']=user_location.y# lat
        list_ =[user_location.x,user_location.y]
        location_es = json.dumps(list_)#f"{user_location.x},{user_location.y}"
        
       
        context["json_user_location_x"] =user_location.x#location_long
        context["json_user_location_y"] =user_location.y#location_lat
    
        return context
class MarkersMapViewTest(TemplateView):

    template_name = "markers/nearbyproducts.html"

    def get_context_data(self, **kwargs):
     
        context = super().get_context_data(**kwargs)
        #filter product
         #----------------------------------
       
        queryset = Product.objects.filter().annotate(distance=Distance('shop__location',  
                                                   user_location)).order_by('distance')[0:6]
    

        context["markers"] = json.loads(serialize("geojson", queryset)) 
        
        list_ =[user_location.x,user_location.y]
        #location_es = json.dumps(list_)
       
        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
    
        return context

class CreateMarkers(LoginRequiredMixin,CreateView):
    model = Marker
    form_class = MarkerForm
    template_name = 'markers/input.html'

    def get(self, request, *args, **kwargs):        
        context={}       
        context["form"] = self.form_class        
        return render(request, self.template_name, context)
       

    def form_valid(self, form):       
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        #filter product
      
        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
    
        return context



class Home(ListView):
    model = Marker
    context_object_name = 'shops'
    
    queryset = Shop.objects.annotate(distance=Distance('location',   user_location)
    ).order_by('distance')[0:6]
    template_name = 'shops/index.html'

def data_ajax(request, *args, **kwargs):
    #filter product
    #----------------------------------
   
    queryset = Product.objects.values('name', shopname=F('shop__name'),location=F('locate_shop__location')).annotate(distance=Distance('locate_shop__location',  
                                            user_location)).order_by('distance')[0:6].values('name','location')
    #values() function has _meta data and cannot work with serilizers
    queryset = Product.objects.annotate(shopname=F('shop__name'),location=F('locate_shop__location')).annotate(distance=Distance('locate_shop__location',  
                                            user_location)).order_by('distance')[0:6]
    
    queryset = Product.objects.annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]

    serializers = CustomSerializer()
    data = serializers.serialize(queryset, geometry_field='shop__location', fields=('shop__name', 'shop__location', ))
   
    data =get_map_data()
   
    return JsonResponse(data, safe=False)

from django.contrib.gis.serializers.geojson import Serializer 

class CustomSerializer(Serializer):

    def end_object(self, obj):
        for field in self.selected_fields:
            if field == 'pk':
                continue
            elif field in self._current.keys():
                continue
            else:
                try:
                    if '__' in field:
                        fields = field.split('__')
                        value = obj
                        for f in fields:
                            value = getattr(value, f)
                        if value != obj:
                            self._current[field] = value
                 
                except AttributeError:
                    pass
        super(CustomSerializer, self).end_object(obj)
def get_map_data():
    queryset = Product.objects.select_related('shop').all().annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
    #list(User.objects.all().values_list('username', flat=True)) 
    print('qset1:', len(queryset), queryset[0].__dict__.keys())
    data = serialize(
        'geojson',
        queryset,
        geometry_field='shop__location',
        fields = ('name', ),
    )
    #return JsonResponse(data, safe=False)
    return data




from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry,Point
from rest_framework.decorators import action
from django_filters import rest_framework  as filters
#from .filter import ProductFilter
from .models import  Marker
from store.models import Product

from . serializers import  MarkerSerializer, ProductSerializer

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
            data['error'] =  "form not valid!"
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

@method_decorator(login_in_user_only_with_routing(), name='dispatch')   
class ProductLocationSlugView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 3. Retrieve
    def get(self, request,  *args, **kwargs):
        slug =  self.kwargs.get('slug')
        x =  self.kwargs.get('x')
        y =  self.kwargs.get('y')
        user_location = Point(float(x), float(y),srid=4326)
        product_queryset = Product.objects.filter(Q(description__icontains =slug)).annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
  
        serializer = ProductSerializer(product_queryset, many=True)
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
class MarkerLocationView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    # 3. Retrieve
    def get(self, request, *args, **kwargs):
         #----------------------------------
        marker_queryset = Marker.objects.annotate(distance=Distance('location',  
                                                   user_location)).order_by('distance')[0:6]

        serializer = MarkerSerializer(marker_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

   
# ----our clients dont pass here but leapfrog to their page
#import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

class ProductLocationView2(LoginRequiredMixin, generic.TemplateView):
    template_name = 'markers/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #----------------------------------
        # product_queryset = Product.objects.annotate(distance=Distance('shop__location',  
        #                                     user_location)).order_by('distance')[0:6]
  
        # context['product_qs'] = product_queryset

        # serializer = ProductSerializer(product_queryset, many=True)
        # context['json_product_qs'] =serializer.data

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

