from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Product
from accounts.models import Review
from django.core.files.uploadedfile import SimpleUploadedFile

class CatalogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=100,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        self.review = Review.objects.create(user=self.user, product=self.product, rating=5, comment='Amazing!')

    def test_product_display(self):
        response = self.client.get(reverse('catalog'))
        self.assertContains(response, 'Test Product')

    def test_review_display(self):
        response = self.client.get(reverse('view_reviews', args=[self.product.id]))
        self.assertContains(response, 'Amazing!')
        self.assertContains(response, '5')




