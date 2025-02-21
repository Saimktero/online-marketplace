# Обработчики запросов (views.py) → API-логика (GET, POST, PUT, DELETE).

from rest_framework import generics, status
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from core.tasks import send_order_confirmation_email


# вьюха Category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


# вьюха Product
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    filterset_fields = ['category']
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


# вьюха Order
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.select_related('user').prefetch_related('products')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    permission_classes = [IsAuthenticated]  # Любой авторизованный пользователь может создать заказ

    def get_queryset(self):
        """
            Обычные пользователи видят только свои заказы, админы – все.
        """
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)  # Обычный пользователь – только свои

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

        print(f'✅ Email пользователя перед отправкой в Celery: "{order.user.email}"')  # Логируем email перед отправкой

        if order.user.email and order.user.email.strip():  # Проверяем, не пустой ли email
            send_order_confirmation_email.delay(order.user.email)  # Запуск задачи в Celery
            print(f'📨 Задача на отправку email добавлена в Celery для "{order.user.email}"')
        else:
            print(f'⚠ Email отсутствует у пользователя "{order.user.username}", задача не отправлена')


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related('user').prefetch_related('products')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Только владелец заказа или админ


# Вьюха User
class UserCreateListView(generics.ListCreateAPIView):
    queryset = User.objects.prefetch_related('ordersп')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




"""""# Попытка привести к нижнему регистру фильтр
def get_queryset(self):
    queryset = super().get_queryset()
    name = self.request.GET.get('name')
    if name:
        queryset = queryset.filter(name_icontains=name.lower()) # Приводим к нижнему регистру
    return queryset"""""
