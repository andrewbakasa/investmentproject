from django.urls import include, path
from django.views.generic import TemplateView


from django.urls import path
from . import views


urlpatterns = [
    
  
    # users
    path('view_model_beef/<int:model_id>/', views.general_page.add_model_specs_page, name="view_model_beef"), 
    path('view_model_beef_mentor/<int:model_id>/', views.general_page.add_model_specs_page_mentor, name="view_model_beef_mentor"), 
  
    path('check_view_model_beef/<int:model_id>/', views.general_page.check_run_requirements_ajax, name="check_model_beef"), 
  
    #Model FeedLotDesignparameters
    path('add_model_feedlotdesignparameters_ajax/', views.general_page.add_model_feedlotdesignparameters_ajax, name="add_model_feedlotdesignparameters_ajax"),
    path('edit_model_feedlotdesignparameters_ajax/<int:id>/', views.general_page.edit_model_feedlotdesignparameters_ajax, name="edit_model_feedlotdesignparameters_ajax"),
   
      
    #get selected model spreadsheet
    path('get_beef_model_spreadsheets/<int:model_id>/', views.usermodels.get_model_spreadsheets, name="get_beef_model_spreadsheets"),
   
]
