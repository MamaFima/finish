from django.contrib import admin
from .models import Profile, Order, Review  # Предположим, что все модели в одном приложении

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email')  # Настройки отображения полей Profile

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product__name')
    actions = ['mark_as_completed']

    @admin.action(description="Пометить как выполненные")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating')



