from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
  
    path('auth/', include('allauth.urls')),
    path('manifest.json', TemplateView.as_view(template_name='silverstrike/manifest.json'),
         name='manifest'),

]
