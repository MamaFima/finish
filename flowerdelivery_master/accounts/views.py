# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from catalog.models import Product
from .forms import ProfileForm, OrderForm
from orders.models import Order  # Используем Order из приложения orders


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    # Получаем заказы текущего пользователя
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})


@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            # Заполняем данные заказчика перед сохранением заказа
            order.customer_name = request.user.profile.get_full_name()
            order.customer_phone = request.user.profile.phone
            order.save()
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Проверьте данные и попробуйте еще раз.')
    else:
        # Предварительное заполнение данных заказчика для формы
        form = OrderForm(initial={
            'customer_name': request.user.profile.get_full_name(),
            'customer_phone': request.user.profile.phone,
        })

    return render(request, 'orders/create_order.html', {'form': form, 'product': product})

# accounts/views.py



