from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from accounts.models import Profile
from orders.models import Order
from catalog.models import Product
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.create(user=self.user, phone='123456789')
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_order_display_in_profile(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            status='ordered',
            delivery_date=timezone.now().date(),
            delivery_time=timezone.now().time(),
            customer_name="Test Customer",
            customer_phone="123456789"
        )
        # Проверки теста...

    def test_order_status_display(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            status='completed',
            delivery_date=timezone.now().date(),
            delivery_time=timezone.now().time(),
            customer_name="Test Customer",
            customer_phone="123456789"
        )
        # Проверки теста...

# Аналогичные изменения для тестов в других приложениях


    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone, '123456789')

    def test_order_display_in_profile(self):
        Order.objects.create(user=self.user, product=self.product, status='ordered')
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Заказ №')
        self.assertContains(response, 'Test Product')

    def test_order_status_display(self):
        order = Order.objects.create(user=self.user, product=self.product, status='completed')
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'Выполнен')  # проверяем статус на русском
        self.assertContains(response, f'Заказ №{order.id}')
