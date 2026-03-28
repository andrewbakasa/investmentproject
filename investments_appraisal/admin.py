from django.contrib import admin
from .models import * # This already imports ModelCategory

# Register simple models
admin.site.register(UserModel)
admin.site.register(TimingAssumption)
admin.site.register(Prices)
admin.site.register(Depreciation)
admin.site.register(Financing)
admin.site.register(WorkingCapital)
admin.site.register(Taxes)
admin.site.register(MacroeconomicParameters)
admin.site.register(Currency)
admin.site.register(ContactUs)
admin.site.register(Downloads)
admin.site.register(UserProfile)
admin.site.register(ModelCategoryDetails)
admin.site.register(Events)
admin.site.register(PurchasePlan)
admin.site.register(SimulationParameters)

# Custom Admin for ModelCategory
@admin.register(ModelCategory)
class ModelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'uniqueid', 'hits')
    
    # help_text in models.py is better, but this works for the form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        uniqueid_field = form.base_fields.get('uniqueid')
        if uniqueid_field:
            uniqueid_field.widget.attrs['placeholder'] = 'e.g. fish001, beef011, greenhouse008'
            uniqueid_field.widget.attrs['style'] = 'font-family: monospace; text-transform: lowercase; color: #d63384;'
            uniqueid_field.help_text = "CRITICAL: Must match a folder name (e.g., fish001). No spaces."
        return form
