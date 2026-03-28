from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(InvestmentBlog)
admin.site.register(BlogItem)