
# Register your models here.
from django.contrib import admin
from accounts.models import Profile  # Исправленный импорт для Profile
from accounts.models import Review  # Импортируем Review из правильного приложения
from .models import Order





@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'product', 'customer_name', 'customer_phone',
        'recipient_name', 'recipient_phone', 'delivery_address',
        'delivery_date', 'delivery_time', 'status', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_editable = ('status',)  # Позволяет редактировать статус прямо в списке
    actions = ['mark_as_completed']

    @admin.action(description="Пометить как выполненные")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')



# orders/admin.py



