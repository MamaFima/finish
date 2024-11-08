# accounts/urls.py

from django.urls import path
from . import views  # Это импорт из orders


app_name = 'orders'  # Устанавливает пространство имен

urlpatterns = [
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('add_review/<int:order_id>/', views.add_review, name='add_review'),
    path('write_review/<int:product_id>/', views.write_review, name='write_review'),
    # Здесь маршруты только для orders
]








