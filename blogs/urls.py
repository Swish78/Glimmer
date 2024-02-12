from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogReviewCreateView,
    BlogReviewUpdateView,
    BlogReviewDeleteView,
)

app_name = 'blogs'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('<int:pk>/reviews/create/', BlogReviewCreateView.as_view(), name='blog_review_create'),
    path('reviews/<int:pk>/update/', BlogReviewUpdateView.as_view(), name='blog_review_update'),
    path('reviews/<int:pk>/delete/', BlogReviewDeleteView.as_view(), name='blog_review_delete'),
    # Add more views as needed
]
