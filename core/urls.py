# Маршруты (urls.py) → Определяют пути API (/api/orders/, /api/products/).

from django.urls import path, include
from .views import (CategoryListCreateView, CategoryDetailView,
                    ProductListCreateView, ProductDetailView,
                    OrderListCreateView, OrderDetailView,
                    UserCreateView, UserLoginView, UserCreateListView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings


# Эндпоинты Category
urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]

# Эндпоинты Product
urlpatterns += [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]

# Эндпоинты Order
urlpatterns += [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]

# Эндпоиинты User
urlpatterns += [
    path('users/register/', UserCreateView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserCreateListView.as_view(), name='user-list-create'),
]

# Debug
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]