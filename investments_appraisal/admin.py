from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(UserModel)
admin.site.register(TimingAssumption)

admin.site.register(Prices)

admin.site.register(Depreciation)
admin.site.register(Financing)
admin.site.register(WorkingCapital)
admin.site.register(Taxes)
admin.site.register(MacroeconomicParameters)
admin.site.register(ModelCategory)

admin.site.register(Currency)
admin.site.register(ContactUs)
admin.site.register(Downloads)
admin.site.register(UserProfile)
admin.site.register(ModelCategoryDetails)
admin.site.register(Events)


admin.site.register(PurchasePlan)

