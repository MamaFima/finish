# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product
from accounts.models import Review  # Импортируем модель отзывов
from django.db.models import Avg



def catalog(request):
    products = Product.objects.all()
    for product in products:
        reviews = product.reviews.all()
        product.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'catalog/catalog.html', {'products': products})





def view_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'catalog/view_reviews.html', {'product': product, 'reviews': reviews})

