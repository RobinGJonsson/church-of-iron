from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.sessions.models import Session

from .forms import OrderForm
from profiles.forms import UserProfileForm
from .models import Order, OrderItem
from gym.models import Gym
from profiles.models import UserProfile
from store.models import Product
from gym.models import Membership
from global_context.cart_content import cart_content

from datetime import datetime
import stripe
import json


# Gets called from stripe.js to initialize stripe
@ csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@ csrf_exempt
def create_checkout_session(request):
    # If it's a post get the shipping data and save it to the session to use in the checkout success
    shipping_data = {}
    if request.method == 'POST':
        rq = request.POST
        # If save info is in the session save this data to the profile
        # Allow the option to save their info

        shipping_data = {
            'full_name': rq['full_name'],
            'email': rq['email'],
            'phone': rq['phone'],
            'address': rq['address'],
            'apartment_number': rq['apartment_number'],
            'city': rq['city'],
            'county': rq['county'],
            'postcode': rq['postcode'],
        }

        request.session['shipping_data'] = shipping_data
        if 'save-info' in rq:
            request.session['save_info'] = rq['save-info']
    domain_url = settings.DOMAIN_URL
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        # Items will be collected from session storage
        membership_data = request.session.get('membership_data', {})
        cart = request.session.get('cart', {})
        # Create stripe product and price so that they cannot be manipulated
        # Go through cart items and membership signup
        line_items = []
        if membership_data:
            price = int(membership_data['price'] * 100)

            stripe_product = stripe.Product.create(
                name=f"{membership_data['membership']} membership")
            stripe_price = stripe.Price.create(
                product=stripe_product, unit_amount=price, currency=settings.STRIPE_CURRENCY)

            line_items.append({
                'price': stripe_price,
                'quantity': 1,
            })

        for id, quantity in cart.items():
            product = Product.objects.get(id=id)
            price = int(product.price * 100)

            stripe_product = stripe.Product.create(name=product.name)
            stripe_price = stripe.Price.create(
                product=stripe_product, unit_amount=price, currency=settings.STRIPE_CURRENCY)

            line_items.append({
                'price': stripe_price,
                'quantity': quantity,
            })

        # Create the session
        checkout_session = stripe.checkout.Session.create(
            success_url=f'{domain_url}checkout/checkout-success/',
            cancel_url=f'{domain_url}',
            payment_method_types=['card'],
            mode='payment',
            line_items=line_items,
            metadata={
                'membership': json.dumps(membership_data),
                'cart': json.dumps(cart),
                'shipping_data': json.dumps(shipping_data),
            }
        )

        # Send the data to the js file
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})


def checkout_view(request):
    """ View to display the final contents of what is being purchased """
    # Get the cart content and the membership_data from the session
    cart = request.session.get('cart', {})
    membership_data = request.session.get('membership_data', {})

    if not cart and not membership_data:
        messages.info(request, "You don't have anything to checkout yet!")
        return redirect(reverse('home'))

    payment_plan = None
    membership = None
    gym = None
    form = None
    starting_date = datetime.now().date()

    # If it is a store item, it needs a shipping form
    if cart:
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            form = OrderForm(instance=user_profile)
        else:
            form = OrderForm()

    if membership_data:
        payment_plan = membership_data['payment_plan']
        membership = Membership.objects.get(name=membership_data['membership'])
        gym = membership_data['gym']
        if not gym:
            gym = 'All Gyms'

        if payment_plan == 'monthly':
            payment_plan = f'{membership.monthly_price}/month'
        elif payment_plan == 'yearly':
            payment_plan = f'{membership.yearly_price}/year'

    context = {
        'payment_plan': payment_plan,
        'membership': membership,
        'form': form,
        'gym': gym,
        'starting_date': starting_date,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request):
    """ View save the order and to display the order summary when it has been paid for """

    order = None
    gym = None
    user_profile = None
    membership = None
    payment_plan = None

    cart = request.session.get('cart', {})
    shipping_data = request.session.get('shipping_data', {})
    membership_data = request.session.get('membership_data', {})
    save_info = request.session.get('save_info', {})

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)

    # Save the order
    if cart:
        # Create the order
        order_form = OrderForm(shipping_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user_profile = user_profile
                print(user_profile)
            order.save()
            print(order.user_profile)

            # Connect order items to the order
            for id, quantity in cart.items():
                product = Product.objects.get(id=id)

                if product.has_size:
                    item_by_size = quantity['item_by_size']
                    # If the product has size loop through the sizes and get the qunatity of each size
                    for size, size_quantity in item_by_size.items():
                        order_item = OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=size_quantity,
                            product_size=size
                        )
                        order_item.save()
                else:
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        product_size=None
                    )
                    order_item.save()

    # Save the membership to the user
    if membership_data:
        membership = Membership.objects.get(
            name=membership_data['membership'])

        # Assign the membership and payment_plan to the user profile
        user_profile.membership = membership
        user_profile.payment_plan = membership_data['payment_plan']

        # Register the user as a member at the appropriate gym/gyms
        if membership.level < 3:
            gym = Gym.objects.get(name=membership_data['gym'])
            gym.members.add(user_profile)
            gym = gym.name
        else:
            gyms = Gym.objects.all()
            for gym in gyms:
                gym.members.add(user_profile)
            gym = 'All Gyms'

        user_profile.save()

        payment_plan = user_profile.payment_plan

        if payment_plan == 'monthly':
            payment_plan = f'{membership.monthly_price}/month'
        elif payment_plan == 'yearly':
            payment_plan = f'{membership.yearly_price}/year'

    # Save shipping info to user profile if they want
    if save_info:
        form = UserProfileForm(shipping_data, instance=user_profile)

        if form.is_valid():
            form.save()

    context = {
        'shipping_data': shipping_data,
        'order': order,
        'gym': gym,
        'membership': membership,
        'payment_plan': payment_plan,
        'user_profile': user_profile
    }

    # Delete all sessions
    if 'cart' in request.session:
        del request.session['cart']
    if 'save_info' in request.session:
        del request.session['save_info']
    if 'membership_data' in request.session:
        del request.session['membership_data']
    if 'shipping_data' in request.session:
        del request.session['shipping_data']

    return render(request, 'checkout/checkout_success.html', context)
