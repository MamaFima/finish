from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from orders.models import Order
from catalog.models import Product
from django.urls import reverse

class OrderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=100)

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            delivery_date=timezone.now().date(),
            delivery_time=timezone.now().time(),
            customer_name="Test Customer",
            customer_phone="123456789",
            status='completed')
        self.assertEqual(order.status, 'ordered')
        self.assertEqual(order.customer_name, 'Test Customer')

    def test_add_review(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            status='completed',
            delivery_date=timezone.now().date(),
            delivery_time=timezone.now().time()
        )
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('orders:write_review', args=[self.product.id]), {'rating': 5, 'review': 'Great product!'})
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(order.product.reviews.first().rating, 5)

    def test_status_change(self):
        order = Order.objects.create(user=self.user, product=self.product, status='ordered')
        order.status = 'completed'
        order.save()
        self.assertEqual(Order.objects.get(id=order.id).status, 'completed')
