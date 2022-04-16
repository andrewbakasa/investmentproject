from django.urls import include, path
from django.views.generic import TemplateView


from django.urls import path
from . import views



urlpatterns = [
    path('users_last_login/', views.general_page.get_users_last_login, name="ulogin"),
    path('get_users_last_login_ajax/', views.general_page.get_users_last_login_ajax, name="get_users_last_login_ajax"),
  
    path('home/', views.general_page.home_page, name="home_page"),
    path('models/', views.general_page.user_models, name="user_models"),
    path('display_models/', views.general_page.display_models, name="display_pagination"),
    path('display_models_ajax/', views.general_page.display_models_ajax, name="display_models_ajax"),
    path('display_models_ajax_filter/<str:slug>/', views.general_page.display_models_ajax_filter, name="display_models_ajax_filter"),

    path('display_projects_ajax/', views.general_page.display_projects_ajax, name="display_projects_ajax"),
    path('investment/', views.general_page.index, name='investments_start_page'),     
   
    path('update_model/<str:pk>/', views.general_page.usermodel_update_ajax, name="update_model"),
    
   
    path('entry/create/businessmodel/', views.general_page.UserBusinessModelCreate.as_view(),  name='create_businessmodel'),              
    path('entry/save/businessmodel/', views.general_page.create_usermodel_instance,  name='save_new_businessmodel'),              
    path('ujax/', views.general_page.create_usermodel_ajax, name="create_usermodel_ajax"),
  
    # users
    #----divet to appropriate app
    #FISH?
    #BEEF?
    path('select_model/<int:model_id>/',views.general_page.select_model_specs_page, name="select_model"),
    path('select_model_mentor/<int:model_id>/',views.general_page.select_model_specs_page_mentor, name="select_model_mentor"),
    
    path('check_count_ajax', views.general_page.check_count_ajax, name="check_count_ajax_method"),
   
    #Timing Assumptions
    path('add_model_timing_assumptions_ajax/<int:model_id>/', views.general_page.add_model_timing_assumptions_ajax, name="add_model_timing_assumptions_ajax"),
    path('edit_model_timing_assumptions_ajax/<int:model_id>/<int:ta_id>/', views.general_page.edit_model_timing_assumptions_ajax, name="edit_model_timing_assumptions_ajax"),
   

   #Model Prices
    path('add_model_prices_ajax/<int:model_id>/', views.general_page.add_model_prices_ajax, name="add_model_prices_ajax"),
    path('edit_model_prices_ajax/<int:model_id>/<int:price_id>/', views.general_page.edit_model_prices_ajax, name="edit_model_prices_ajax"),
   
   #Model Depreciation
    path('add_model_depreciation_ajax/<int:model_id>/', views.general_page.add_model_depreciation_ajax, name="add_model_depreciation_ajax"),
    path('edit_model_depreciation_ajax/<int:model_id>/<int:depr_id>/', views.general_page.edit_model_depreciation_ajax, name="edit_model_depreciation_ajax"),
   
    #Model Taxes
    path('add_model_taxes_ajax/<int:model_id>/', views.general_page.add_model_taxes_ajax, name="add_model_taxes_ajax"),
    path('edit_model_taxes_ajax/<int:model_id>/<int:taxes_id>/', views.general_page.edit_model_taxes_ajax, name="edit_model_taxes_ajax"),
   
    #Model Financing
    path('add_model_financing_ajax/', views.general_page.add_model_financing_ajax, name="add_model_financing_ajax"),
    path('edit_model_financing_ajax/<int:id>/', views.general_page.edit_model_financing_ajax, name="edit_model_financing_ajax"),
   
    #Model WorkingCapital
    path('add_model_workingcapital_ajax/', views.general_page.add_model_workingcapital_ajax, name="add_model_workingcapital_ajax"),
    path('edit_model_workingcapital_ajax/<int:id>/', views.general_page.edit_model_workingcapital_ajax, name="edit_model_workingcapital_ajax"),
   
    #Model MacroEconomicParameters
    path('add_model_macroeconomicparameters_ajax/', views.general_page.add_model_macroeconomicparameters_ajax, name="add_model_macroeconomicparameters_ajax"),
    path('edit_model_macroeconomicparameters_ajax/<int:id>/', views.general_page.edit_model_macroeconomicparameters_ajax, name="edit_model_macroeconomicparameters_ajax"),
   
  
   path('delete_bussiness_model_ajax/<int:model_id>/<int:page_no>/', views.general_page.delete_bussiness_model_ajax, name="delete_bussiness_model"),
   
  
    # new records
    path('update/user_pref/',
        views.general_page.update_user_pref,  name='update_user_pref'),

    path('update/user_pref/ajax/',
        views.general_page.update_user_pref_ajax,  name='update_user_pref_ajax'),

    path('update/user_profile/ajax/',
        views.general_page.update_user_profile_ajax,  name='update_user_profile_ajax'),
     
    path('update_model_likes/<int:id>/',
        views.general_page.update_model_likes_ajax,  name='update_model_likes'),

    path('contact_us/ajax/',
        views.general_page.contact_us_ajax,  name='contact_us_ajax'),  
    
    path('news_subscribe/ajax/',
        views.general_page.news_subscribe_ajax,  name='news_subscribe_ajax'),  
    
   
    path('upload/user_pref/',
        views.general_page.upload_form_user_pref,  name='upload_form_user_pref'),  

    path('upload/user_profile/',
        views.general_page.upload_form_user_profile,  name='upload_form_user_profile'),

    path('', views.general_page.index, name="index"),#Home
    path('about/', views.general_page.about, name="about"),
    path('projects/', views.general_page.projects, name="projects"),
    
    path('project_search/<str:slug>/',
        views.general_page.project_search_ajax,  name='project_search_ajax'), 

    path('umodels/', views.general_page.models, name="models"),
    path('experts/', views.general_page.experts, name="experts"),
    path('events/', views.general_page.events, name="events"),
    path('pricing/', views.general_page.pricing, name="pricing"),
    path('contact/', views.general_page.contact, name="contact"),
    path('project-details/<int:id>/', views.general_page.project_details, name="project-details"),
    # path('model-details/<int:id>/', views.general_page.model_details, name="model-details"),

    path('search/', views.general_page.search, name="search"),
 
]
