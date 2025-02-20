from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import Product, Category
from django.contrib.auth.models import User
from django.urls import reverse


class ProductAPITest(APITestCase):
    """Тестирование API товаров"""

    def setUp(self):
        """Создаём тестовые данные"""
        self.client = APIClient()

        # Создаём категори
        self.category = Category.objects.create(name='Electronics')

        # Создаём пользователей
        self.user = User.objects.create_user(username='testuser', password='testuser123')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        # Создаём тестовый товар
        self.product = Product.objects.create(
            name='Laptop',
            category=self.category,
            price=999.99
        )

        # URL-ы API
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.id})

    def test_get_product_list(self):
        """Проверяем, что список товаров доступен всем"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) # Должен быть один товар

    def test_get_product_detail(self):
        """Проверяем, что можно получить конкретный товар"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)  # Название должно совпадать

    def test_create_product_admin(self):
        """Проверяем, что админ может создавать товары"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Smartphone',
            'category': self.category.id,
            'price': 499.99
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)  # Должно быть 2 товара

    def test_create_product_user_forbidden(self):
        """Проверяем, что обычный пользователь не может создать товар"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Smartphone',
            'category': self.category.id,
            'price': 499.99
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_admin(self):
        """Проверяем, что админ может изменить товар"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Updated Laptop'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Laptop')

    def test_update_product_user_forbidden(self):
        """Проверяем, что обычный пользователь НЕ может изменить товар"""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Laptop'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_admin(self):
        """Проверяем, что админ может удалять товар"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())  # Товар должен быть удалён

    def test_delete_product_user_forbidden(self):
        """Проверяем, что обычный пользователь НЕ может удалить товар"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())