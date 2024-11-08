from django.test import TestCase
from catalog.models import Product
from accounts.models import Review
from django.urls import reverse
from django.contrib.auth.models import User

class CatalogTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=100)

    def test_product_display(self):
        response = self.client.get(reverse('catalog'))
        self.assertContains(response, 'Test Product')

    def test_review_display(self):
        Review.objects.create(user=self.user, product=self.product, rating=5, comment='Amazing!')
        response = self.client.get(reverse('catalog'))
        self.assertContains(response, 'Amazing!')
        self.assertContains(response, '5')
