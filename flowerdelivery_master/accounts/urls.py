# accounts/urls.py
# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),  # Страница профиля пользователя
]




