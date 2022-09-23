from django.contrib.gis.db import models as geo_models
from django import forms
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from store.models import Product, Shop
from .models import Marker, TradedCurrency
from django.contrib.gis.geos import GEOSGeometry
from django.forms import ModelForm, Textarea
LEAFLET_WIDGET_ATTRS = {
    'map_height': '200px',
    'map_width': '200px',#'50%',
    'display_raw': 'true',
    'map_srid': 4326,
}

LEAFLET_FIELD_OPTIONS = {'widget': LeafletWidget(attrs=LEAFLET_WIDGET_ATTRS)}

FORMFIELD_OVERRIDES = {
    geo_models.PointField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiPointField: LEAFLET_FIELD_OPTIONS,
    geo_models.LineStringField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiLineStringField: LEAFLET_FIELD_OPTIONS,
    geo_models.PolygonField: LEAFLET_FIELD_OPTIONS,
    geo_models.MultiPolygonField: LEAFLET_FIELD_OPTIONS,
}
import re
#from django.contrib.gis import forms
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis import forms as gisforms
from leaflet.forms.fields import PointField



class ShopForm0(gisforms.ModelForm):
    lat = gisforms.FloatField(required=False, label='Latitude')
    lng = gisforms.FloatField(required=False, label='Longtitude')
    location = gisforms.PointField(
        srid=4326,
        widget=gisforms.OSMWidget(
            attrs={'map_width': 800, 'map_height': 500, 'default_zoom': 15}
        )
    )
    class Meta:
        #widgets = {'location': LeafletWidget()}
        model = Shop
        exclude = ['', ]
        widgets = {
            'address': Textarea(attrs={'cols': 30, 'rows': 3}),
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # location = self.initial.get("location", None)
        # if isinstance(location, Point):
        #     self.initial["lng"], self.initial["lat"] = location.tuple

        instance= kwargs.get('instance', None) 
        if instance:
            if instance.location:
                #self.fields['user']=initial_arguments.user
                self.fields["lng"], self.fields["lat"] = instance.location.tuple


    def clean(self):
        data = super().clean()
        if set(self.changed_data)>={"lat","lng"}:
            lat, lng = data.pop("lat", None), data.pop("lng", None)
            data["location"] = Point(lng, lat, srid=4326)
    
        if not ("location" in data or ("lat" in data and  "lng" in data)):
            raise forms.ValidationError(
                {"location": "No coordinates."})
        return data
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin


# class ParkForm(forms.ModelForm):
#     class Meta:
#         model = Parks
#         fields = ('park_name_en', 'description', 'picture',)
#         geom = forms.PolygonField()
class SimplePointField(gisforms.Field):
    default_error_messages = {
        'invalid': _('Enter latitude,longitude'),
    }
    re_point = re.compile(r'^\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\s*$')

    def prepare_value(self, value):
        if isinstance(value, Point):
            return "{},{}".format(*value.coords)
        return value

    def to_python(self, value):
        """
        Validates input. Returns a Point instance or None for empty values.
        """
        value = super(SimplePointField, self).to_python(value)
        if value in self.empty_values:
            return None
        try:
            m = self.re_point.match(force_text(value))
            if not m:
                raise ValueError()
            value = Point(float(m.group(1)), float(m.group(2)))
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'],
                                  code='invalid')

        return value

# usage exmaple:
class MyForm(forms.Form):
    point = SimplePointField()  # this one is required
    other_point = SimplePointField(required=False)  # can stay blank


class MarkerForm(forms.ModelForm):
    formfield_overrides = FORMFIELD_OVERRIDES
    class Meta:
        model = Marker
        fields = ('name', 'location')
        widgets = {'location': LeafletWidget()}



#from leaflet.forms.fields import PolygonField

from django.contrib.gis import forms  as gisform

class PointEntryOrSelectForm(forms.ModelForm):
   
    class Meta:
        model = Shop
        fields = ['user', 'name', 'location', 'address','city']
        widgets = {'location': LeafletWidget()}
        widgets = {
            'address': Textarea(attrs={'cols': 30, 'rows': 3}),
        }


class ShopForm2(gisforms.ModelForm):
    location = gisforms.PointField(widget=gisforms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
   
    class Meta:
        widgets = {'location': LeafletWidget()}
        model = Shop
        fields = ['user', 'name', 'location', 'address','city']
        widgets = {
            'address': Textarea(attrs={'cols': 30, 'rows': 3}),
        }

class ShopForm1(gisforms.ModelForm):
    lat = gisforms.FloatField(required=False, label='Latitude')
    lng = gisforms.FloatField(required=False, label='Longtitude')
    #location = PointField()
    #location = SimplePointField()
    class Meta:
        model = Shop
        fields = ('user', 'name', 'location', 'address','city')
        widgets = {'location': LeafletWidget()}
        widgets = {
            'address': Textarea(attrs={'cols': 30, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        print('MMMMDATA', kwargs)
        if 'data' in kwargs :
            #coordinate = kwargs['data'].pop('location', None)
            coordinate = None
            if 'location' in kwargs['data']:
                coordinate = kwargs['data']['location']
            if coordinate:
                coordinate = coordinate.replace(',', '')  # remove comma, as we need single space between two numbers.
                kwargs['data']['location'] = f'SRID=4326;POINT({coordinate})'
                print(kwargs['data']['location'])

        super(ShopForm, self).__init__(*args, **kwargs)  

    def clean(self):
        data = super().clean()
        print('.............', data)
        if set(self.changed_data)>={"lat","lng"}:
            lat, lng = data.pop("lat", None), data.pop("lng", None)
            data["location"] = Point(lng, lat, srid=4326)
    
        if not ("location" in data or ("lat" in data and "lng" in data)):
            raise forms.ValidationError(
                {"location": "No coordinates."})
        return data
    def clean_location(self):
        coordinates = self.cleaned_data['location']
        latitude, longitude = coordinates.split(', ', 1)
        return GEOSGeometry('POINT('+longitude+' '+latitude+')')
class ShopForm(forms.ModelForm):
    formfield_overrides = FORMFIELD_OVERRIDES
    lat = forms.FloatField(required=True, label='Latitude')
    lng = forms.FloatField(required=True, label='Longtitude')
   
    class Meta:
        model = Shop
        fields = ['name', 'address','city']
        widgets = {
            'address': Textarea(attrs={'cols': 30, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # location = self.initial.get("location", None)
        # if isinstance(location, Point):
        #     self.initial["lng"], self.initial["lat"] = location.tuple
        instance= kwargs.get('instance', None) 
        if instance:
            if instance.location:
                #self.fields['user']=initial_arguments.user
                self.lng, self.lat = instance.location.tuple
                #self.lng, self.lat = instance.location.tuple
                print(self.lng, self.lat)
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

class TradedCurrencyForm(forms.ModelForm):
    description = forms.CharField(
                    help_text=" Describe the use",#text to help
                    widget=forms.Textarea( attrs={
                    'cols'          : "30", #size
                    'rows'          : "3", #size
                    'placeholder'   : 'Description', 
                    'style'         : 'resize : none' 
                    }))
    class Meta:
        model = TradedCurrency
        fields = ['currency_offered', 'currency_expected', 'rate_expected', 'description','value' , 'created_by']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        initial_arguments= kwargs.get('initial', None) 
        #print("kwargs",kwargs)
        user=None
        if initial_arguments:
            if initial_arguments['created_by']:
                user=initial_arguments['created_by']

        super(TradedCurrencyForm,self).__init__(*args, **kwargs)
        

class TradedCurrencyFormUpdate(forms.ModelForm):
    description = forms.CharField(
                    help_text=" Describe the use",#text to help
                    widget=forms.Textarea( attrs={
                    'cols'          : "30", #size
                    'rows'          : "3", #size
                    'placeholder'   : 'Description', 
                    'style'         : 'resize : none' 
                    }))
    class Meta:
        model = TradedCurrency
        fields = ['currency_offered', 'currency_expected', 'rate_expected', 'description','value' ]

    def clean_currency_expected(self): 
         #print(data)
        currency_expected = self.cleaned_data['currency_expected'] 
        if currency_expected != None:
            if 'currency_offered' in self.cleaned_data:
                currency_offered = self.cleaned_data['currency_offered']
                if currency_offered == currency_expected:
                    raise ValidationError(_(f'Same currency is not feasible'))
                return currency_expected
        return currency_expected
            

    def clean_currency_offered(self): 
         #print(data)
        currency_offered = self.cleaned_data['currency_offered'] 
        if currency_offered != None:
            if 'currency_expected' in self.cleaned_data:
                currency_expected = self.cleaned_data['currency_expected']
                if currency_expected == currency_offered:
                    raise ValidationError(_(f'Same currency is not feasible'))
                return currency_offered
        return currency_offered
            