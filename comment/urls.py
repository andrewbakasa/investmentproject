from django.urls import path
from django.views.generic import TemplateView

# We use TemplateView.as_view() as a placeholder for all routes
urlpatterns = [
    # Main Blog List
    path('i-blogs/', TemplateView.as_view(template_name="dummy.html"), name="investment-blogs"),
    
    # Detail View
    path('post/<int:pk>/', TemplateView.as_view(template_name="dummy.html"), name='blog-detail'),
    
    # User Posts
    path('user/0/dummy/', TemplateView.as_view(template_name="dummy.html"), name='user-blogs'),
    
    # Create / Update / Delete
    path('blog/new/', TemplateView.as_view(template_name="dummy.html"), name='blog-create'),
    path('blog/update/', TemplateView.as_view(template_name="dummy.html"), name='blog-update'),
    path('blog/delete/', TemplateView.as_view(template_name="dummy.html"), name='blog-delete'),
]

# from django.urls import include, path
# from django.views.generic import TemplateView


# from django.urls import path
# # from . import views

# # from .views import ( PostListView, PostDetailView, 
# #                     PostCreateView,  PostUpdateView, 
# #                     PostDeleteView, UserPostListView
# #           )

# # urlpatterns = [
# #     path('i-blogs/<int:id>/', PostListView.as_view(), name="investment-blogs"),    
# #     path('post/<int:pk>/', PostDetailView.as_view(), name='blog-detail'),
# #     path('user/<int:id>/<str:username>/', UserPostListView.as_view(), name='user-blogs'),
# #     path('blog/<int:id>/new/', PostCreateView.as_view(), name='blog-create'),
# #     path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='blog-update'),
# #     path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='blog-delete'),
    
# # ]

