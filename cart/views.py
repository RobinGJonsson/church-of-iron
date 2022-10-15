from django.shortcuts import render, redirect


def cart_view(request):

    context = {

    }

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, item_id):

    qunatity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += qunatity
    else:
        cart[item_id] = qunatity

    request.session['cart'] = cart
    print(request.session['cart'])

    return redirect(redirect_url)
