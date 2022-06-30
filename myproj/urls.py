from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', include('investments_appraisal.urls')),
    path('acc/', include('silverstrike.urls')),
    path('admin/', admin.site.urls),
    path('common/', include('common.urls')),
    path('tr/', include('trading.urls')),
    path('forum/', include('businessforum.urls')),
    path('beef/', include('beefapp.urls')),
    path('fish/', include('fishapp.urls')),
    path('comment/', include('comment.urls')),
    #path('api/', include('comment.api.urls')),  # only required for API Framework
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

