from django.shortcuts import render, redirect


def cart_view(request):

    context = {

    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, item_id):

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
            else:
                cart[item_id]['item_by_size'][size] = quantity
        else:
            cart[item_id] = {'item_by_size': {size: quantity}}
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

    request.session['cart'] = cart

    return redirect(redirect_url)
