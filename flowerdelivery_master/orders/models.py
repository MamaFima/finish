
# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from catalog.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Оформлен'),
        ('delivery', 'На доставке'),
        ('completed', 'Выполнен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=20)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ordered')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ №{self.id} - {self.product.name} для {self.recipient_name}"
