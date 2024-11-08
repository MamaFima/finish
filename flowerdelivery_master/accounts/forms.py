# accounts/forms.py
from django import forms
from .models import Profile, Order

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'surname', 'first_name', 'middle_name', 'phone', 'email']
        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class OrderForm(forms.ModelForm):
    recipient_name = forms.CharField(label="ФИО Получателя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipient_phone = forms.CharField(label="Телефон Получателя", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_date = forms.DateField(label="Дата доставки", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    delivery_time = forms.TimeField(label="Время доставки", widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    delivery_address = forms.CharField(label="Адрес доставки", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['product', 'recipient_name', 'recipient_phone', 'delivery_date', 'delivery_time', 'delivery_address']
        widgets = {'product': forms.HiddenInput()}

