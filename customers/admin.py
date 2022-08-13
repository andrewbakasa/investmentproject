from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(SalesPlan)
admin.site.register(SalesPlanItem)
admin.site.register(CompanyUser)
admin.site.register(Employee)
admin.site.register(Tag)