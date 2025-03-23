# Сериализаторы (serializers.py) → Преобразуют данные в JSON.

from rest_framework import serializers
from .models import Category, Product, Order, OrderItem
from django.contrib.auth.models import User


# Базовый сериализатор
class BaseModelSerializers(serializers.ModelSerializer):
    class Meta:
        abstract = True


# Категории
class CategorySerializer(BaseModelSerializers):
    class Meta:
        model = Category
        fields = '__all__'


# Товары
class ProductSerializer(BaseModelSerializers):
    class Meta:
        model = Product
        fields = '__all__'


# Позиция заказа
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product')

    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity']


# Заказ
class OrderSerializer(BaseModelSerializers):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = self.initial_data.get('items', [])
        order = Order.objects.create(user=user)

        total = 0
        for item_data in items_data:
            product_id = item_data['product_id']
            product = Product.objects.get(id=product_id.id if hasattr(product_id, 'id') else product_id)
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total += product.price * quantity

        order.total_price = total
        order.save()
        return order


# Пользователи
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
        return Order.objects.select_related('user').prefetch_related('items__product').all()


