from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework.authtoken import views as drf_views

urlpatterns = [
  
    path('auth/', include('allauth.urls')),
    path('manifest.json', TemplateView.as_view(template_name='silverstrike/manifest.json'),
         name='manifest'),

]
