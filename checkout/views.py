from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout_view(request):

    cart = request.session.get('cart', {})

    # Prevent access to checkout page through url if cart is empty
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect, reverse('store_view')

    form = OrderForm()
    context = {
        'stripe_public_key': 'pk_test_51LpDQpIzVos11sjSUcEHLZcpRnV3ep3d7G1pFDjVkNDFiPnJt3mQMtlbwLGwRpK8Mskdek33PYosJICOUKkAot6v009s6I71Qh',
        'client_secret': 'client secret',
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context)
