
from django.urls import include, path
from django.views.generic import TemplateView
from . import views
from common.views import (
    #CreateUserView,
    DocumentDeleteView,
    DocumentDetailView,
    DocumentListView,
    
    # ProfileView,
    # UpdateUserView,
    # UserDeleteView,
    # UserDetailView,
    # UsersListView,

    document_create,
    document_update,
    download_attachment,
    download_document,
    landing_page,
    HomeView,
    ProfileView,
)

app_name = "common"




urlpatterns = [
    path("", landing_page, name="landing_page"),
    
    path("dashboard/", HomeView.as_view(), name="dashboard"),
    # path("profile/", ProfileView.as_view(), name="profile"),
  
  
    # Document
    path("documents/", DocumentListView.as_view(), name="doc_list"),
    path("documents/create/", document_create, name="create_doc"),
    path("documents/<int:pk>/edit/", document_update, name="edit_doc"),
    path("documents/<int:pk>/view/", DocumentDetailView.as_view(), name="view_doc"),
    path("documents/<int:pk>/delete/", DocumentDeleteView.as_view(), name="remove_doc"),
    # download
    path("documents/<int:pk>/download/", download_document, name="download_document"),
    # download_attachment
    path(
        "attachments/<int:pk>/download/",
        download_attachment,
        name="download_attachment",
    ),
  
] 