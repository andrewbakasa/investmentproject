from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Investment)
admin.site.register(Investor)
admin.site.register(Enterprenuer)
admin.site.register(InvestmentCategory)
admin.site.register(InvestmentDetails)
admin.site.register(Tag)
