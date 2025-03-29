from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import Category
from django.contrib.auth.models import User


class TestCategoryAPI(APITestCase):

    def setUp(self):
        Category.objects.all().delete()
        # Инициализируем клиент, чтобы делать запросы
        self.client = APIClient()

        # Создаём тестового пользователя (обычный и админ)
        self.user = User.objects.create_user(username='testuser123', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin123', password='admin123')

        # Создаём тестовую категорию
        self.category = Category.objects.create(name='Test Category')

        # URL'ы API (формируются через reverse, чтобы не хардкодить)
        self.list_url = reverse('category-list')  # api/categories/
        self.detail_url = reverse('category-detail', args=[self.category.id])  # api/categories/1

    # тесты на get (список и детальный просмотр)
    def test_get_category_list(self):
        """Проверяем, что список категорй доступен всем"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Должна быть одна категория

    def test_get_category_detail(self):
        """Проверяем, что можно получить конкретную категорию"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    #   тест на post (создание категории, только для админов)
    def test_create_category_unauthorized(self):
        """Неавторизованный пользователь не может создать категорию"""
        data = {'name': 'New Category'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Должен быть 401

    def test_create_category_admin(self):
        """Администратор может создать категорию"""
        self.client.force_authenticate(user=self.admin_user)
        date = {'name': 'New Category'}
        response = self.client.post(self.list_url, date, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    # тест на patch (изменение категории, только для админов)
    def test_update_category_unauthorizate(self):
        """Обычный пользователь не может изменить категорию"""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Category'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_admin(self):
        """Администратор может изменять категорию"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Update Category'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Update Category')

    # тест на delete (удаление категории, только для админов)
    def test_delete_category_unauthorized(self):
        """Обычный пользователь не может удалить категорию"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_admin(self):
        """Администратор может удалить категорию"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
