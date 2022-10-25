from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from .forms import OrderForm
from profiles.forms import UserProfileForm
from .models import Order, OrderItem
from profiles.models import UserProfile
from store.models import Product
from gym.models import Membership
from global_context.cart_content import cart_content

import stripe
import json


@require_POST
# Save extra data to the payment intent
def cache_checkout_data(request):
    try:
        # Payment Intent Data
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)


def checkout_view(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    membership_data = request.session.get('membership_data', {})
    print(membership_data)

    refund = 0
    payment_plan_change_cost = 0

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'address': request.POST['address'],
            'apartment_number': request.POST['apartment_number'],
            'county': request.POST['county'],
        }

        form = OrderForm(form_data)
        if form.is_valid():
            order = form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            # Releate an orderitem to an order for use in Order History
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_item = OrderItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('cart_view'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))

    else:
        # Prevent access to checkout page through url if cart is empty
        if not cart:
            messages.error(
                request, "There's nothing in your cart at the moment")
            return redirect(reverse('products'))

        current_cart = cart_content(request)
        total = float(current_cart['grand_total'])

        if membership_data:
            if 'cost_of_change' in membership_data:
                total += membership_data['cost_of_change']
            if 'payment_plan_change_cost' in membership_data:
                payment_plan_change_cost = membership_data['payment_plan_change_cost']
            if 'refund' in membership_data:
                refund = membership_data['refund']

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        user = request.user
        if user.is_authenticated:
            user = UserProfile.objects.get(user=user)
            form = OrderForm(instance=user)
        else:
            form = OrderForm()

    context = {
        'form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'payment_plan_change_cost': payment_plan_change_cost,
        'refund': refund,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    membership_data = request.session.get('membership_data', {})

    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'full_name': order.full_name,
                'phone': order.phone_number,
                'email': order.email,
                'postcode': order.postcode,
                'city': order.town_or_city,
                'address': order.address,
                'apartment_number': order.street_address2,
                'county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

        if membership_data:
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            membership = Membership.objects.get(
                name=membership_data['membership'])
            user_profile_form(membership=membership)
            if user_profile_form.is_valid():
                user_profile_form.save()
                print('Membership paid for and updated ')

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']
    if 'refund' in request.session:
        del request.session['refund']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
