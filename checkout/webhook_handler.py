from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItem
from gym.models import Membership, Gym
from profiles.models import UserProfile
from store.models import Product

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, purchase, user_profile=None, gym=None):
        """Send the user a confirmation email"""
        if gym:
            if user_profile.payment_plan == 'monthly':
                price = purchase.monthly_price
            elif user_profile.payment_plan == 'yearly':
                price = purchase.yearly_price

            customer_email = user_profile.email
            subject = render_to_string(
                'checkout/confirmation_emails/membership_confirmation_email_subject.txt',
                {'purchase': purchase})
            body = render_to_string(
                'checkout/confirmation_emails/membership_confirmation_email_body.txt',
                {'purchase': purchase,
                 'price': price,
                 'contact_email': settings.DEFAULT_FROM_EMAIL,
                 'gym': gym,
                 'user_profile': user_profile})

        else:
            customer_email = purchase.email
            subject = render_to_string(
                'checkout/confirmation_emails/store_confirmation_email_subject.txt',
                {'purchase': purchase})
            body = render_to_string(
                'checkout/confirmation_emails/store_confirmation_email_body.txt',
                {'purchase': purchase,
                 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        print('in webhook success ')
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        membership_data = intent.metadata.membership

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        # Try to get a successful event from stripe for 5 seconds
        print(1, shipping_details)

        if cart:
            while attempt <= 5:
                try:
                    print(2, shipping_details)
                    order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        email__iexact=billing_details.email,
                        phone__iexact=shipping_details.phone,
                        postcode__iexact=shipping_details.address.postal_code,
                        city__iexact=shipping_details.address.city,
                        address__iexact=shipping_details.address.line1,
                        apartment_number__iexact=shipping_details.address.line2,
                        county__iexact=shipping_details.address.state,
                        grand_total=grand_total,
                    )
                    order_exists = True
                    break

                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

        attempt = 1
        membership_signup_successfull = False
        if membership_data:
            while attempt < 5:
                try:
                    membership = Membership.objects.get(
                        name=membership['membership'])

                    user_profile = UserProfile.objects.get(
                        id=membership_data['user_profile_id'],
                        membership=membership,
                        payment_plan=membership_data['payment_plan'],
                    )

                    gym = Gym.objects.filter(
                        members=user_profile
                    )

                    if membership.value < 3:
                        if len(gym) != 1:
                            attempt += 1
                            time.sleep(1)
                            continue

                    # If the membership is gold or higher the user
                    # should be assigned to all gym
                    elif membership.value >= 3:
                        if len(gym) <= 1:
                            attempt += 1
                            time.sleep(1)
                            continue

                    membership_signup_successfull = True
                except Exception as e:
                    print(e)
                    attempt += 1
                    time.sleep(1)

        if order_exists or membership_signup_successfull:
            if len(gym) > 1:
                gym = 'All Gyms'
            else:
                gym = gym[0]

            if order_exists:
                email = order.email
                self._send_confirmation_email(order, email)
            if membership_signup_successfull:
                email = user_profile.email
                self._send_confirmation_email(
                    membership, email, user_profile=user_profile, gym=gym)

            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        else:
            if cart:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        phone=shipping_details.phone,
                        postcode=shipping_details.address.postal_code,
                        city=shipping_details.address.city,
                        address=shipping_details.address.line1,
                        apartment_number=shipping_details.address.line2,
                        county=shipping_details.address.state,
                    )
                    for item_id, item_data in json.loads(cart).items():
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
                    email = order.email
                    self._send_confirmation_email(membership, email)

                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500)

            if membership_data:
                try:
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

                    email = user_profile.email
                    self._send_confirmation_email(
                        membership, email, user_profile=user_profile, gym=gym)

                except Exception as e:
                    print(e)
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500)

        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created order in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
