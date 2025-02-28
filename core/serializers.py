# Сериализаторы (serializers.py) → Преобразуют данные в JSON.

from rest_framework import serializers
from .models import Category, Product, Order
from django.contrib.auth.models import User


# Базовый сериализатор с общей логикой
class BaseModelSerializers(serializers.ModelSerializer):
    """
    Базовый сериализатор для упрощения кода и наследования общих настроек.
    """
    class Meta:
        abstract = True


# Работа с моделью Category
class CategorySerializer(BaseModelSerializers):
    class Meta:
        model = Category
        fields = '__all__'


# Работа с моделью Product
class ProductSerializer(BaseModelSerializers):
    class Meta:
        model = Product
        fields = '__all__'


# Работа с моделью Order
class OrderSerializer(BaseModelSerializers):
    total_price = serializers.SerializerMethodField()
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'products', 'total_price', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'total_price']

    def create(self, validated_data):
        """
            Автоматически устанавливаем пользователя, создавшего заказ.
        """
        validated_data['user'] = self.user
        return super().create(validated_data)

    @staticmethod
    def get_total_price(obj):
        """
            Автоматически вычисляет сумму заказа по продуктам.
        """
        return sum(product.price for product in obj.products.all())


# Работа с моделью User
class UserSerializer(BaseModelSerializers):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs ={
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        """
        Создание пользователя с хешированным паролем.
        """
        user = User.objects.create_user(**validated_data)
        return user


# Оптимизация запросов для заказов с использованием select_related и prefetch_related
class OptimizedOrderSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        model = Order
        fields = OrderSerializer.Meta.fields

    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('products').all()


