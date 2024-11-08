# orders/forms.py

from django import forms
from .models import Order  # Убираем Review
from accounts.models import Review  # Импортируем Review из правильного приложения


class OrderForm(forms.ModelForm):
    recipient_name = forms.CharField(label="ФИО Получателя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipient_phone = forms.CharField(label="Телефон Получателя", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_date = forms.DateField(label="Дата доставки", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    delivery_time = forms.TimeField(label="Время доставки", widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    delivery_address = forms.CharField(label="Адрес доставки", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['recipient_name', 'recipient_phone', 'delivery_date', 'delivery_time', 'delivery_address']




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Оценка',
            'comment': 'Комментарий',
        }
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
