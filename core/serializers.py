# Сериализаторы (serializers.py) → Преобразуют данные в JSON.

from rest_framework import serializers
from .models import Category, Product, Order
from django.contrib.auth.models import User


# Работа с моделью Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Работа с моделью Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Работа с моделью Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# Работа с моделью User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Создание пользователя с хешированным паролем
        return user
