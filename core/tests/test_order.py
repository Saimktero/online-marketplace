from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from core.models import Product, Category, Order
from django.contrib.auth.models import User
from django.urls import reverse


class OrderAPITest(APITestCase):
    def setUp(self):

        self.client = APIClient()

        self.category = Category.objects.create(name='Electronics')

        self.product1 = Product.objects.create(
            name='Laptop',
            category=self.category,
            price=1000
        )
        self.product2 = Product.objects.create(
            name='Smartphone',
            category=self.category,
            price=500
        )

        self.user = User.objects.create_user(username='testuser', password='testuser123')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        self.order = Order.objects.create(
            user=self.user
        )
        self.order.products.set([self.product1, self.product2])

        self.list_url = reverse('order-list')
        self.detail_url = reverse('order-detail', kwargs={'pk': self.order.id})

    def test_get_order_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_order_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'products': [self.product1.id, self.product2.id]
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_order_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'products': [self.product1.id]}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.products.count(), 1)

    def tests_delete_order_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_delete_order_user_forbidden(self):
        """юзер не может удалить чужой заказ"""
        another_user = User.objects.create_user(username='anotheruser', password='another123')
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Order.objects.filter(id=self.order.id).exists())


