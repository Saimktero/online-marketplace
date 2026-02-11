# Обработчики запросов (views.py) → API-логика (GET, POST, PUT, DELETE).

from rest_framework import generics, status, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.core.management import call_command
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from core.tasks import send_order_confirmation_email
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, UserSerializer
from .models import Category, Product, Order
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .filters import ProductFilter
import os


# Базовые классы для упрощения кода
class BaseListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]


class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]


# вьюха Category
class CategoryListCreateView(BaseListCreateView):
    queryset = Category.objects.prefetch_related('products').all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


# вьюха Product
class ProductListCreateView(BaseListCreateView):
    queryset = Product.objects.select_related('category').order_by('id').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    filterset_fields = ['category']
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class ProductDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


# вьюха Order
# @method_decorator(cache_page(60 * 50), name='dispatch')


class OrderListCreateView(BaseListCreateView):
    queryset = Order.objects.select_related('user').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_queryset(self):
        """
            Обычные пользователи видят только свои заказы, админы – все.
        """
        cache_key = f'user_orders_{self.request.user.id}'
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            print('\n ✅ Данные взяты из кеша')
            return cached_queryset

        # Если в кеше нет данных, делаем запрос в БД
        qs = super().get_queryset().select_related('user').prefetch_related('items__product')

        if self.request.user.is_staff:
            result = qs
        else:
            result = qs.filter(user=self.request.user).only('id', 'user', 'total_price', 'created_at')

        cache.set(cache_key, result, 60 * 15)
        return result

    def get_serializer_context(self):
        """
            Передаём request в сериализатор, чтобы он мог установить user.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        """Создаём заказ и вызываем фоновую задачу для отправки email"""
        order = serializer.save()
        order.refresh_from_db()

        # ❗ Очищаем кэш, чтобы обновился список
        cache_key = f'user_orders_{order.user.id}'
        cache.delete(cache_key)
        print(f'🧹 Кэш очищен: {cache_key}')

        if order.user.email:
            send_order_confirmation_email.delay(order.user.email)  # Запуск задачи в Celery
            print(f'📨 Задача на отправку email добавлена в Celery для "{order.user.email}"')


@method_decorator(cache_page(60 * 15), name='dispatch')
class OrderDetailView(BaseRetrieveUpdateDestroyView):
    queryset = Order.objects.select_related('user').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]  # Только владелец заказа или админ


# Вьюха User
class UserCreateListView(BaseListCreateView):
    queryset = User.objects.prefetch_related('orders').all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    """
    Аутентификация пользователя
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Делаем миграции для Railway
"""
class TriggerMigrateView(View):
    def get(self, request):
        if os.environ.get("ENV") == "production":
            try:
                call_command("migrate")
                return JsonResponse({"status": "migrated"})
            except Exception as e:
                return JsonResponse({"status": "error", "detail": str(e)}, status=500)
        return JsonResponse({"status": "ignored (not production"})
"""

# Создание суперпользователя для Railway
"""
class CreateSuperuserView(View):
    def get(self, request):
        if os.environ.get("ENV") == "production":
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="password1415"
                )
                return JsonResponse({"status": "created", "user": "admin"})
            return JsonResponse({"status": "already exists"})
        return JsonResponse({"status": "ignored (not production"})
"""

# Тест отправки письма от Celery
"""
class TestEmailView(View):
    def get(self, request):
        try:
            send_mail(
                'Проверка отправки письма',
                'Если ты это читаешь - email работает',
                'priluckijkirill30@gmail.com',
                ['priluckijkirill30@gmail.com'],
                fail_silently=False
            )
            return JsonResponse({'status': 'Письмо отправлено успешно'})
        except Exception as e:
            return JsonResponse({'status': 'Ошибка отправки', 'error': str(e)}, status=500)
"""

"""# Попытка привести к нижнему регистру фильтр
def get_queryset(self):
    queryset = super().get_queryset()
    name = self.request.GET.get('name')
    if name:
        queryset = queryset.filter(name_icontains=name.lower()) # Приводим к нижнему регистру
    return queryset"""
