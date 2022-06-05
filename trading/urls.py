from django.urls import include, path
from django.views.generic import TemplateView


from django.urls import path
from . import views



urlpatterns = [
    
   # users

    path('', views.home, name="trading_home"), 
    path('view/<int:model_id>/', views.project_details, name="view_trading"),
    path('investor-details/<int:id>/<int:investment_id>/', views.investor_details, name="investor-details"), 
    path('investment-details/<int:id>/', views.investment_details, name="investment-details"), 
    path('edit-investment/<int:id>/', views.edit_investment, name="edit-investment"), 
    path('view-investors/<int:id>/', views.view_investors, name="view-investors"),
  
    path('display_investment_ajax/', views.display_investment_ajax, name="display_investment_ajax"),
    path('display_business_ajax/', views.display_business_ajax, name="display_business_ajax"),
     path('display_myinvestment_ajax/', views.display_myinvestment_ajax, name="display_myinvestment_ajax"),

    path('investment_search/<str:tag_id_or_slug>/', views.investment_search_ajax, {'search_type': ''}, name='investment_search_ajax'), 
    path('investment_search/<str:tag_id_or_slug>/tags/', views.investment_search_ajax,{'search_type': 'tags'}, name='investment_search_tag_ajax'), 
    path('investment_search/<str:tag_id>/<str:slug>/search/tags/', views.investment_search_and_tags_ajax,{'search_type': 1}, name='investment_search_and_tags_ajax'), 
    path('investment_search/<str:tag_id>/tags/', views.investment_search_and_tags_ajax,{'search_type': 0}, name='investment_tags_ajax'), 

    path('t/<str:tag_id>/', views.investment_load_tags, name='investment_load_tags'), 
    path('t/search/<str:tagname>/<str:search_str>/', views.investment_load_tags_search_string, name='investment_load_tags_search_string'),
    
    path('update_investment_likes/<int:id>/',views.update_investment_likes_ajax,  name='update_investment_likes'),
    path('u/i/', views.get_user_investments, name="user_investments"),
    path('u/b/', views.get_user_businesses, name="user_businesses"),

    path('u_investment_jax/', views.create_userinvestment_ajax, name="create_userinvestment_ajax"),
    path('u_investor_jax/', views.create_userinvestor_ajax, name="create_userinvestor_ajax"),
    path('update_investor/<str:pk>/', views.userinvestor_update_ajax, name="update_investor"),
    path('delete_investor_ajax/<int:id>/<int:page_no>/', views.delete_investor_ajax, name="delete_investor_ajax"),
  
    path('u_business_jax/', views.create_userbusiness_ajax, name="create_userbusiness_ajax"),
    path('delete_investment_ajax/<int:id>/<int:page_no>/', views.delete_investment_ajax, name="delete_investment_ajax"),
    path('update_investment_ajax/<str:pk>/', views.update_investment_ajax, name="update_investment_ajax"),
    
    path('edit_model_investment_paragraph_ajax/<int:id>/', views.edit_model_investment_paragraph_ajax, name="edit_model_investment_paragraph_ajax"),
    path('add_model_investment_paragraph_ajax/<int:id>/', views.add_model_investment_paragraph_ajax, name="add_model_investment_paragraph_ajax"),
  
  
]
