from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile
from orders.models import Order
from catalog.models import Product
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileTest(TestCase):
    def setUp(self):
        # Удаляем профиль, если он уже существует, и создаем нового пользователя
        self.user = User.objects.create(username='testuser')
        Profile.objects.filter(user=self.user).delete()

        # Создаем новый профиль пользователя
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

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone, '123456789')


