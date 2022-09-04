"""Markers view."""

from http.client import HTTPResponse
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.db.models import F

import json

from django.core.serializers import serialize
from django.views.generic.base import TemplateView

from markers.forms import MarkerForm
from store.models import Product, Shop

from .models import Marker
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render

from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

longitude =-20.756114
latitude = 27.553711

user_location = Point(longitude, latitude, srid=4326)
class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "markers/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        queryset = Marker.objects.annotate(distance=Distance('location',  
                                                   user_location)).order_by('distance')[0:6]

        for i in  queryset:
            print(f"{i.name}, {i.location}, {i.distance}")                                           
        print('her is same', queryset)


        context["markers"] = json.loads(serialize("geojson", queryset))


        print(context["markers"]) 
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        #----------------------------FOR TESTING::::::::-------
        #--------------------------------------------------
        queryset = Product.objects.annotate(shopname=F('shop__name'),location=F('shop__location')).annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
          
        for i in  queryset:
            print(f"{i.shopname}, {i.location}, {i.distance}")         
        context["markers"] = json.loads(serialize("geojson", queryset, fields=('name','location', 'distance'))) 
        #----------------------------------------------------
        #--------------------------------------------------
        print(user_location)
        dict_={}
        dict_['x']=user_location.x
        dict_['y']=user_location.y
        list_ =[user_location.x,user_location.y]
        location_es = json.dumps(list_)#f"{user_location.x},{user_location.y}"
        
        print(location_es)
        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
    
        return context
class MarkersMapViewTest(TemplateView):
    """Markers map view."""

    template_name = "markers/test.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        #filter product
        queryset = Product.objects.filter().annotate(distance=Distance('shop__location',  
                                                   user_location)).order_by('distance')[0:6]
        print("****************************************")
        print(queryset, queryset.count() )    
        for i in  queryset:
            print(f"{i.name},  {i.distance}") 

        context["markers"] = json.loads(serialize("geojson", queryset)) 
        print(context["markers"])
        print("****************************************")
        list_ =[user_location.x,user_location.y]
        location_es = json.dumps(list_)#f"{user_location.x},{user_location.y}"
       
        context["json_user_location_x"] =user_location.x#location_es
        context["json_user_location_y"] =user_location.y#location_es
    
        return context

class CreateMarkers(LoginRequiredMixin,CreateView):
    model = Marker
    form_class = MarkerForm
    template_name = 'markers/input.html'

    def get(self, request, *args, **kwargs):
        # investment = get_object_or_404(Marker,pk=self.kwargs.get('id'))
        # investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)
        # form = self.form_class(initial={'user': investmentblog })
        
        context={}
        # id=investmentblog.investment.id
        # investment = get_object_or_404(Investment,pk=id)
        # context["investment"] = investment
        # context["investment_id"] = id
        context["form"] = self.form_class
        
        return render(request, self.template_name, context)
       

    def form_valid(self, form):
        #investment = get_object_or_404(Investment,pk=self.kwargs.get('id'))
        #investmentblog, created=InvestmentBlog.objects.get_or_create(investment=investment)
       
        #form.instance.author = self.request.user
        #form.instance.investmentblog = investmentblog
        return super().form_valid(form)


class Home(ListView):
    model = Marker
    context_object_name = 'shops'
    queryset = Shop.objects.annotate(distance=Distance('location',   user_location)
    ).order_by('distance')[0:6]
    template_name = 'shops/index.html'

def data_ajax(request, *args, **kwargs):
    #filter product
    queryset = Product.objects.values('name', shopname=F('shop__name'),location=F('locate_shop__location')).annotate(distance=Distance('locate_shop__location',  
                                            user_location)).order_by('distance')[0:6].values('name','location')
    #values() function has _meta data and cannot work with serilizers
    queryset = Product.objects.annotate(shopname=F('shop__name'),location=F('locate_shop__location')).annotate(distance=Distance('locate_shop__location',  
                                            user_location)).order_by('distance')[0:6]
    
    queryset = Product.objects.annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
  
   
                                    
    # print(queryset, queryset.count() )    
    # for i in  queryset:
    #     print(f"{i}, {i}, {i.distance}")         
    # data = json.loads(serialize("geojson", queryset, geometry_field=('shop__location'),fields=('shop__name',))) 
    # # serialize('geojson', City.objects.all(),
    # #       geometry_field='point',
    # #       fields=('name',))
    print("I ma her.......................................")

    serializers = CustomSerializer()
    data = serializers.serialize(queryset, geometry_field='shop__location', fields=('shop__name', 'shop__location', ))
    print(data) 
    print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNn')
    data =get_map_data()
    print(data)
        #return HTTPResponse(data, content_type="application/json")
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

"""World borders API views."""
from rest_framework import viewsets
from rest_framework_gis import filters


#from .models import WorldBorder
#from .serializers import WorldBorderSerializer


# class WorldBorderViewSet(viewsets.ReadOnlyModelViewSet):
#     """World border view set."""

#     bbox_filter_field = "mpoly"
#     filter_backends = (filters.InBBoxFilter,)
#     queryset = WorldBorder.objects.all()
#     bbox_filter_include_overlapping = True
#     serializer_class = WorldBorderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class ProductLocationView(APIView):
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 3. Retrieve
    def get(self, request,  *args, **kwargs):
      
        #product = Product.objects.filter(product__id = product_id)
        product_queryset = Product.objects.annotate(distance=Distance('shop__location',  
                                            user_location)).order_by('distance')[0:6]
  
        serializer = ProductSerializer(product_queryset, many=True)
        print("in AAAAAAAAAAAAAAAAAAa")
        print(serializer, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MarkerLocationView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    # 3. Retrieve
    def get(self, request, *args, **kwargs):
        marker_queryset = Marker.objects.annotate(distance=Distance('location',  
                                                   user_location)).order_by('distance')[0:6]

        serializer = MarkerSerializer(marker_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

   


