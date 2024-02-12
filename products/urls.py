from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductSearchView,
    add_review,
    update_review,
    delete_review

)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
    path('<int:pk>/add_review/', add_review, name='add_review'),
    path('<int:pk>/update_review/<int:review_pk>/', update_review, name='update_review'),
    path('<int:pk>/delete_review/<int:review_pk>/', delete_review, name='delete_review'),
    # Add more views as needed
]
