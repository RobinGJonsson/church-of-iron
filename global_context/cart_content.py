from decimal import Decimal
from django.conf import settings


def cart_content(request):

    cart_items = []
    total = 0
    cart_count = 0

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = total * \
            Decimal(settings.FREE_DELIVERY_PERCENTAGE / 100)
        spend_for_free_delivery = settings.FREE_DELIVERY_THRESHOLD - delivery_cost
    else:
        delivery_cost = 0

    grand_total = delivery_cost + total

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'grand_total': grand_total,
        'spend_for_free_delivery': spend_for_free_delivery,
    }

    return context
