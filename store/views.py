from django.shortcuts import render
from .models import Category, Product


def store(request):

    products = Product.objects.all()
    categories = None

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'store/store.html', context)
