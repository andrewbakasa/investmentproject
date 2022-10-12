

from django.urls import  include, path

from . import views
from django.views.generic import TemplateView

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'productsapi', views.ProductViewSet)
from .views import (
    ProductLocationView,
    ProductLocationSlugView,
    MapView,
    ProductLocationViewLandingPage,
    add_shop,
    ShopUpdateView,
    CurrencyTradingLocationViewLandingPage,
    CurrencyLocationView,
    TradedCurrencyLocationSlugView
)
urlpatterns = [
    path('api_geofind/<str:x>/<str:y>/<str:pageno>/', ProductLocationView.as_view(),  name='locate_product_api'),
    path('api_geofind/tag/<str:slug>/<str:x>/<str:y>/<str:pageno>/', ProductLocationSlugView.as_view(),  name='locate_product_api_slug'),
    path('p/geo/s/', ProductLocationViewLandingPage.as_view(),  name='geo_find_product_landing'),
    path('add/w/', add_shop,  name='add_shop'),
    path('s/<int:pk>/u/', ShopUpdateView.as_view(), name='shop-update'),
    path('c/tr/', CurrencyTradingLocationViewLandingPage.as_view(),  name='currency_trade_landing'),
    path('api_currency/<str:x>/<str:y>/<str:adj>/', CurrencyLocationView.as_view(),  name='locate_currency_api'),
    path('api_currency/tag/<str:slug>/<str:x>/<str:y>/<str:adj>/', TradedCurrencyLocationSlugView.as_view(),  name='locate_currency_api_slug'),
    
    path('traded_currency_ajax/', views.create_tc_ajax, name="create_tc_ajax"),
    path('tc_update/', views.tc_update, name="update_tc"),

  
    path('tag_currency_ajax/<str:target_id>/', views.create_user_currency_tag_ajax, name="create_currency_tag_ajax"),
    path('complete_currency_ajax/<str:owner_id>/', views.complete_currency_ajax, name="complete_currency_ajax"),
    path('update_nearby_user_ajax/', views.update_nearby_user_ajax, name="update_nearby_user_ajax"),
    # path('display_investment_ajax/', views.display_investment_ajax, name="display_investment_ajax"),
  

]

