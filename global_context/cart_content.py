from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from store.models import Product


def cart_content(request):

    cart_items = []
    cart_total = 0
    cart_count = 0
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        product = get_object_or_404(Product, id=item_id)

        # If item data is an int the item data is quantity
        if isinstance(item_data, int):
            cart_total += item_data * product.price
            cart_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            for size, quantity in item_data['items_by_size'].keys():
                total += quantity * product.price
                cart_count += quantity
                cart_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    if cart_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = cart_total * \
            Decimal(settings.FREE_DELIVERY_PERCENTAGE / 100)
        spend_for_free_delivery = round(
            (settings.FREE_DELIVERY_THRESHOLD - cart_total), 2)
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

    return context
