from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    context = {
        "user_orders": user_orders,
    }
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
            review.comment = form.cleaned_data['comment']  # Используем поле 'comment' для отзыва
            review.rating = form.cleaned_data['rating']
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect("view_reviews", product_id=order.product.id)
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    else:
        form = ReviewForm()
    return render(request, 'orders/add_review.html', {'form': form, 'order': order})


@login_required
def write_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        review_text = request.POST.get("review")

        if rating and review_text:
            review = Review(user=request.user, product=product, rating=rating, comment=review_text)  # Заменяем 'review' на 'comment'
            review.save()
            messages.success(request, 'Ваш отзыв успешно сохранен!')
        else:
            messages.error(request, 'Заполните все поля для отзыва.')
    return redirect("profile")  # Проверьте, что 'profile' — это правильное имя маршрута для профиля


@login_required
def view_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'view_reviews.html', context)
