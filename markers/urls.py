

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
)
urlpatterns = [
    path('map/', views.MarkersMapView.as_view(), name='marker_home'),
    path('create/', views.CreateMarkers.as_view(), name='map'),
    path('p/location/', views.MarkersMapViewTest.as_view(), name='product_location_map_view'),
    # path('ajax/', views.data_ajax, name='data_ajax'),
    path('api_locate_product/', ProductLocationView.as_view(),  name='locate_product_api'),
    #path('api_locate_marker/', MarkerLocationView.as_view(),  name='locate_marker'),
    # path('api/', include(router.urls)),

]

