from django.contrib.gis.db import models as geo_models
from django import forms
from leaflet.forms.widgets import LeafletWidget
from .models import Marker

LEAFLET_WIDGET_ATTRS = {
    'map_height': '500px',
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

class MarkerForm(forms.ModelForm):
    formfield_overrides = FORMFIELD_OVERRIDES
    class Meta:
        model = Marker
        fields = ('name', 'location')
        widgets = {'location': LeafletWidget()}


