from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),     # Маршрут для каталога
    path('reviews/<int:product_id>/', views.view_reviews, name='view_reviews'),
]




