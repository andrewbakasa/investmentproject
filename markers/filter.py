from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from .models import Marker 
from store.models import Product

class ProductFilter(GeoFilterSet):
    subcounty = filters.CharFilter(method= 'get_facilities_by_subcounty')


    class Meta:
        model = Product
        exclude = ['location']

    def get_facilities_by_subcounty(self, queryset, name, value ):
        query_ = Product.objects.filter(pk=value)
        if query_:
            obj = query_.first()
            return queryset.filter(location__within = obj.location)
        return queryset

class RegionFilter(GeoFilterSet):
    slug = filters.CharFilter(name='slug', lookup_expr='istartswith')
    contains_geom = GeometryFilter(name='geom', lookup_expr='contains')

    class Meta:
        model = Product