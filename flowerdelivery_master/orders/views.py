# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .forms import OrderForm
from .forms import ReviewForm
from .models import Order  # Убираем Review
from accounts.models import Review  # Импортируем Review из правильного приложения




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
            order.customer_name = f"{request.user.profile.first_name} {request.user.profile.middle_name} {request.user.profile.surname}"
            order.customer_phone = request.user.profile.phone
            order.save()
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('profile')  # Перенаправление в личный кабинет после оформления заказа
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Проверьте данные и попробуйте еще раз.')
    else:
        # Предварительное заполнение данных заказчика для формы
        form = OrderForm(initial={
            'customer_name': f"{request.user.profile.first_name} {request.user.profile.middle_name} {request.user.profile.surname}",
            'customer_phone': request.user.profile.phone,
        })

    context = {'form': form, 'product': product}
    return render(request, 'orders/create_order.html', context)

@login_required
def orders(request):
    # Получаем заказы текущего пользователя
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/orders.html', {'orders': user_orders})




@login_required
def add_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = order.product
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('profile')
    else:
        form = ReviewForm()

    return render(request, 'orders/add_review.html', {'form': form, 'order': order})


# orders/views.py


@login_required
def write_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    return redirect('profile')

