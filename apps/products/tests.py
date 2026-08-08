from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from apps.products.models import Category, Product, WeightVariant


class ProductsAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            id='cat-test',
            name='Test Meat',
            slug='meat',
            icon_name='Beef'
        )
        self.product = Product.objects.create(
            id='prod-test',
            name='Test Mutton Curry',
            category=self.category,
            price=500.00,
            description='Test description',
            is_popular=True,
            is_ready_to_cook=True,
            preparation_time_minutes=20
        )
        self.weight_variant = WeightVariant.objects.create(
            id='v-test-1',
            product=self.product,
            weight='500g',
            price=500.00,
            stock=10
        )

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['slug'], 'meat')

    def test_list_products_pagination_shape(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 1)

    def test_get_product_detail(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Mutton Curry')
        self.assertIn('weightVariants', response.data)
        self.assertEqual(len(response.data['weightVariants']), 1)

    def test_product_filter_by_category(self):
        response = self.client.get('/api/products/?category=meat')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response_empty = self.client.get('/api/products/?category=nonexistent')
        self.assertEqual(response_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(response_empty.data['count'], 0)
