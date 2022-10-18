from django.urls import  include, path

from . import views
from django.views.generic import TemplateView
#from rest_framework import routers
#from rest_framework.authtoken import views as drf_views
from store import api
urlpatterns = [
    path('dashboard/', views.IndexViewStartPage.as_view(), name='index_startpage'),
    path('', views.store, name='store'),
    path('ml_home', views.store, name='ml_home'),#fix this 26 april 2021. find tis url: useless in system 
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.update_item, name='update_item'),
    path('update_item_ajax/', views.update_item_ajax, name='update_item_ajax'),
    path('empty_cart_ajax/', views.empty_cart_ajax, name='empty_cart_ajax'),
    
    path('process_order/', views.process_order, name='process_order'),
    path('p/d/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search_product', views.search_filter_product, name='store_search_product'),
    # api
    path('api/get_sales_graph_by_day/<dstart>/<dend>/',
         api.get_sales_graph_by_day, name='get_sales_graph_by_day'),

    path('display_product_ajax/', views.display_product_ajax, name="display_product_ajax"),
    path('tag/<str:tag_id>/p/', views.product_load_tags, name='product_load_tags'), 
    path('tag/product/search/<str:tagname>/<str:search_str>/', views.product_load_tags_search_string, name='product_load_tags_search_string'),
 
    path('product_search/<str:tag_id_or_slug>/', views.product_search_ajax, {'search_type': ''}, name='product_search_ajax'), 
    path('product_search/<str:tag_id_or_slug>/tags/', views.product_search_ajax,{'search_type': 'tags'}, name='product_search_tag_ajax'),    
    path('product_search/<str:tag_id>/<str:slug>/search/tags/', views.product_search_and_tags_ajax,{'search_type': 1}, name='product_search_and_tags_ajax'), 
    path('product_search/<str:tag_id>/tags/', views.product_search_and_tags_ajax,{'search_type': 0}, name='product_tags_ajax'), 

]