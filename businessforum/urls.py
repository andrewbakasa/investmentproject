from django.urls import include, path
from django.views.generic import TemplateView


from django.urls import path
from . import views

from .views import ( PostListView, PostDetailView, 
                    PostCreateView,  PostUpdateView, 
                    PostDeleteView, UserPostListView
          )

urlpatterns = [
    path('i-blogs/<int:id>/', PostListView.as_view(), name="investment-blogs"),    
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog-detail'),
    path('user/<int:id>/<str:username>/', UserPostListView.as_view(), name='user-blogs'),
    path('blog/<int:id>/new/', PostCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='blog-delete'),
    
]
