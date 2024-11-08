from django.contrib.auth.models import User
from django.db import models
from catalog.models import Product  # Импорт модели товара из каталога

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    surname = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.surname}".strip()

class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Оформлен'),
        ('delivery', 'На доставке'),
        ('completed', 'Выполнен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
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
        return f"Заказ №{self.id} для {self.recipient_name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} для {self.product.name}"

