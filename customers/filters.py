import django_filters
from django_filters import DateFilter, CharFilter

from store.models import *
from store.models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_ordered", lookup_expr='gte')
    end_date = DateFilter(field_name="date_ordered", lookup_expr='lte')

    # price_lt = django_filters.NumberFilter(field_name="prise", lookup_expr='lt')
    # direction = django_filters.CharFilter(widgets = SelectMultiple(attrs={'class': 'custom-select'}))
    # note = CharFilter(field_name="note", lookup_expr='icontains')
    
    # def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
    #     super(OrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
    #     self.filters['start_date'].field.widget.attrs.update({'class': 'date-input'})
    #     self.filters['end_date'].field.widget.attrs.update({'class': 'date-input'})
    #     self.filters['date_ordered'].field.widget.attrs.update({'class': 'date-input'})
    
    def __init__(self, *args, **kwargs):
        super(OrderFilter,self).__init__(*args, **kwargs)
        initial_arguments= kwargs.get('instance', None)
        if initial_arguments:
            pass
           
    class Meta:
        model = Order
        fields = '__all__'
        exclude = [ 'customer', 'date_created', 'date_ordered', 'transaction_id']


class CustomerFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')
    address1 = CharFilter(field_name="address1", lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = [ 'email', 'phone', 'date_created', 'user', "addrees2"]        