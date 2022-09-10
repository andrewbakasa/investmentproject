from django.contrib import admin

from .models import *


from django.contrib.gis import admin

# @admin.register(Shop)
# class ShopAdmin(LeafletGeoAdmin):
#     form = ShopForm

@admin.register(Shop)
class ShopAdmin(admin.OSMGeoAdmin):
    """Marker admin."""
    pass
    #list_display = ("name", "location")


@admin.register(ShopLocation)
class ShopLocationAdmin(admin.OSMGeoAdmin):
    """Marker admin."""
    pass

    #list_display = ("name", "location")

admin.site.register(Invoice)
admin.site.register(Expense)
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(InvoiceItem)
admin.site.register(InvoiceAttachment)
admin.site.register(ExpenseAttachment)
admin.site.register(Currency)
admin.site.register(CurrencyRate)

admin.site.register(ProductCategory)
#admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OrderAttachment)


# app/admin.py

from import_export import resources

class ProductResource(resources.ModelResource):

    class Meta:
        model = Product    
        exclude = ('image', 'date_created','created_by', )
    #fields = ('id', 'name', 'author', 'price',)
    #export_order = ('id', 'price', 'author', 'name')    


# app/admin.py
from import_export.admin import ImportExportModelAdmin

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

admin.site.register(Product, ProductAdmin)  

admin.site.register(ClientReportAttachment)

admin.site.register(ClientCompany)
