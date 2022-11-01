from django.shortcuts import (
    render, redirect, reverse, HttpResponse)
from django.contrib import messages

from store.models import Product


def cart_view(request):

    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):

    product = Product.objects.get(id=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST.get['product_size']
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if size:
        # If item in cart
        if item_id in list(cart.keys()):
            # If same item with the same size exist in the cart
            if size in cart[item_id]['item_by_size'][size].keys():
                cart[item_id]['item_by_size'][size] += quantity
                messages.success(
                    request, f'Updated size {size.upper} {product.name} quantity')
            else:
                cart[item_id]['item_by_size'][size] = quantity
                messages.success(
                    request, f'Added size {size.upper} {product.name} to the cart')
        else:
            cart[item_id] = {'item_by_size': {size: quantity}}
            messages.success(
                request, f'Added size {size.upper} {product.name} to the cart')
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity')
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {product.name} to the cart')

    request.session['cart'] = cart

    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = Product.objects.get(id=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{product.name} quantity'))
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your cart'))
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity'))
        else:
            cart.pop(item_id)
            messages.success(request,
                             (f'Removed {product.name} '
                              f'from your cart'))

    request.session['cart'] = cart
    return redirect(reverse('cart_view'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""
    try:
        product = Product.objects.get(id=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        cart = request.session.get('cart', {})
        print(cart)
        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {size.upper()} {product.name} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
