from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(ModifiedRecord)
admin.site.register(Vacancy)
admin.site.register(VacancyDuty)
admin.site.register(VacancySkill)
admin.site.register(VacancyOffer)
