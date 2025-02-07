from django.urls import path
from .views import (CategoryListCreateView, CategoryDetailView,
                    ProductListCreateView, ProductDetailView,
                    OrderListCreateView, OrderDetailView)

# Эндпоинт Category
urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]

# Эндпоинт Product
urlpatterns += [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]

# Эндпоинт Order
urlpatterns += [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
