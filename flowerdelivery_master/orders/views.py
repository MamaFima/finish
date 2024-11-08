from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .forms import OrderForm, ReviewForm
from .models import Order
from catalog.models import Product  # Импорт из приложения catalog
from accounts.models import Review  # Импорт из приложения account




@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.customer_name = f"{request.user.profile.first_name} {request.user.profile.middle_name} {request.user.profile.surname}"
            order.customer_phone = request.user.profile.phone
            order.save()
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Проверьте данные и попробуйте еще раз.')
    else:
        form = OrderForm(initial={
            'customer_name': f"{request.user.profile.first_name} {request.user.profile.middle_name} {request.user.profile.surname}",
            'customer_phone': request.user.profile.phone,
        })
    return render(request, 'orders/create_order.html', {'form': form, 'product': product})


@login_required
def orders(request):
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
            messages.error(request, 'Пожалуйста, заполните все поля.')
    else:
        form = ReviewForm()
    return render(request, 'orders/add_review.html', {'form': form, 'order': order})


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Review  # Убедитесь, что Review и Product импортированы

@login_required
def write_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        review_text = request.POST.get("review")

        if rating and review_text:
            review = Review(user=request.user, product=product, rating=rating, review=review_text)
            review.save()
            messages.success(request, 'Ваш отзыв успешно сохранен!')
        else:
            messages.error(request, 'Заполните все поля для отзыва.')
    return redirect("profile")  # Возможно, `profile` — это имя маршрута профиля, проверьте его точность
