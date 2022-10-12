from django.shortcuts import render


def all_products(request):

    return render(request, 'store.store.html')
