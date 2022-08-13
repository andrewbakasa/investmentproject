import django_filters
from django_filters import DateFilter, CharFilter

from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    # price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = [
            'name',
            'digital',
            'categories',
        ]