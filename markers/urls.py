

from django.urls import  include, path

from . import views
from django.views.generic import TemplateView

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'productsapi', views.ProductViewSet)
#router.register(r'markersapi', views.MarkersViewSet)

from .views import (
    # TodoListApiView,
    # TodoDetailApiView,
    ProductLocationView,
    MarkerLocationView,
    ProductLocationSlugView,
    MapView,
    ProductLocationView2,
    
)
urlpatterns = [
    
    #path('', views.park_insert(), name='park_insert'),
    path('map/', views.MarkersMapView.as_view(), name='marker_home'),
    path('createmap/', views.MapViewCreate.as_view(), name='createmap'),
    path('create/', views.CreateMarkers.as_view(), name='map'),
    path('p/l/', views.MarkersMapViewTest.as_view(), name='product_location_map_view'),
    path('api_locate_product/', ProductLocationView.as_view(),  name='locate_product_api'),
    path('api_locate_product2/<str:slug>/', ProductLocationSlugView.as_view(),  name='locate_product_api_slug'),
    path('product/', ProductLocationView2.as_view(),  name='gen_location_product_slug'),
  
   
    #path('api_locate_marker/', MarkerLocationView.as_view(),  name='locate_marker'),
    # path('api/', include(router.urls)),

]

