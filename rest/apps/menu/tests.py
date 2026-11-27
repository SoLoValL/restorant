from django.urls import reverse
from rest_framework.test import APITestCase

from apps.menu.models import Category, Dish


class MenuApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Пицца', slug='pizza', order=1)
        Dish.objects.create(
            category=self.category,
            name='Маргарита',
            slug='margarita',
            description='Классическая пицца',
            price='350.00',
            weight='300 г',
            is_available=True,
            order=1,
        )

    def test_dishes_list(self):
        response = self.client.get(reverse('dish-list'))

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Маргарита')
