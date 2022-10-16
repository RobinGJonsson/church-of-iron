from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from store.models import Product


def cart_content(request):

    cart_items = []
    cart_total = 0
    cart_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        product = get_object_or_404(Product, id=item_id)
        cart_total += quantity * product.price
        cart_count += quantity
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    if cart_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = cart_total * \
            Decimal(settings.FREE_DELIVERY_PERCENTAGE / 100)
        spend_for_free_delivery = settings.FREE_DELIVERY_THRESHOLD - delivery_cost
    else:
        delivery_cost = 0
        spend_for_free_delivery = 0

    grand_total = delivery_cost + cart_total

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'spend_for_free_delivery': spend_for_free_delivery,
    }

    print(spend_for_free_delivery)
    return context
