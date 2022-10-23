from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST


from .models import Gym, GymImage, Membership
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import UpdateMembershipForm
from store.models import Product

import stripe
import json
from datetime import datetime


def all_gyms(request):

    gyms = Gym.objects.all()

    context = {
        'gyms': gyms,
    }

    return render(request, 'gym/all_gyms.html', context)


def gym_details(request, gym_name):

    gym = Gym.objects.get(name=gym_name)
    gym_images = GymImage.objects.filter(gym=gym)
    GOOGLE_MAPS_SECRET_KEY = settings.GOOGLE_MAPS_SECRET_KEY

    context = {
        'gym': gym,
        'gym_images': gym_images,
        'GOOGLE_MAPS_SECRET_KEY': GOOGLE_MAPS_SECRET_KEY,
    }

    return render(request, 'gym/gym.html', context)


def all_memberships(request):

    memberships = Membership.objects.all()

    context = {
        'memberships': memberships,
    }

    return render(request, 'gym/all_memberships.html', context)


def membership(request, membership_name):

    membership = Membership.objects.get(name=membership_name)

    context = {
        'membership': membership,
    }

    return render(request, 'gym/membership.html', context)


def membership_signup(request, membership_name):

    membership = Membership.objects.get(name=membership_name)
    gyms = Gym.objects.all()

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(instance=user_profile)
    else:
        user_profile = request.user
        form = UserProfileForm()

    if request.method == 'POST':
        rq = request.POST
        cart = request.session.get('cart', {})

        # If user does not have an account create an account
        if not request.user.is_authenticated:

            if rq['password1'] == rq['password2']:

                user = authenticate(username=rq['email'],
                                    password=rq['password1'])

                # Create User if they don't exist
                if not user:
                    User.objects.create_user(
                        username=rq['email'],
                        email=rq['email'],
                        password=rq['password1'],
                    )

                user = authenticate(username=rq['email'],
                                    password=rq['password1'])

                login(request, user)
                messages.info(
                    request, f"You are now logged in as {rq['full_name']}.")
                user_profile = UserProfile.objects.get(user=request.user)

            else:
                # Handle wrong passwords diffrently
                return redirect(reverse('membership_signup', args=[membership.name]))

        form_data = {
            'full_name': rq['full_name'],
            'email': rq['email'],
            'phone': rq['phone'],
            'membership': membership,
            'payment_plan': rq['payment_plan'],
        }

        payment_plan = f"{rq['payment_plan'][0]}/{rq['payment_plan'][0]}"
        membership_product = Product.objects.get(
            name=f'{membership.name} membership {payment_plan}')

        cart[membership_product.id] = 1
        request.session['cart'] = cart

        # # Update each value from the form_data to the userprofile
        # for key, value in form_data.items():
        #     setattr(user_profile, key, value)
        # user_profile.save()

        # # Add user to gyms
        # # If bronze or silver add to one choosen gym
        # if 'gyms' in rq:
        #     gym = gyms.get(name=rq['gyms'])
        #     gym.members.add(user_profile)

        # # else add to all gyms
        # else:
        #     for gym in gyms:
        #         gym.members.add(user_profile)

    context = {
        'membership': membership,
        'user_profile': user_profile,
        'form': form,
        'gyms': gyms
    }

    return render(request, 'gym/membership_signup.html', context)


def membership_update(request):
    member = UserProfile.objects.get(user=request.user)
    form = UpdateMembershipForm(instance=member)

    cost_of_change = 0
    membership = member.membership
    last_mshp_chg = member.membership_renewed
    mshp_expires = member.membership_expires_on
    months_remaining = round((mshp_expires - last_mshp_chg).days / 30)

    if request.method == 'POST':
        rq = request.POST

        if 'membership' in rq:
            prev_mshp = membership
            new_mshp = Membership.objects.get(level=rq['membership'])
            current_payment_plan = member.payment_plan

            if current_payment_plan == 'yearly':
                # Refund for the months that are left of the memberships since they already paid for the full year
                refund = ((prev_mshp.yearly_price) / 12) * months_remaining

                cost_of_change += new_mshp.yearly_price - refund
                print(
                    f'Refund ${refund} owed to member when switching from {prev_mshp} membership to a {new_mshp} membership\nTotal membership difference: ${round(cost_of_change, 2)}')

        if 'payment_plan' in rq:
            prev_pp = member.payment_plan
            new_pp = rq['payment_plan']

            if prev_pp != new_pp:
                if prev_pp == 'yearly' and new_pp == 'monthly':
                    monthly_price = membership.monthly_price
                    yearly_price_month_avg = membership.yearly_price / 12
                    price_diff = float(monthly_price) - yearly_price_month_avg

                    cost_of_change += price_diff * months_remaining
                    print(
                        f'Extra ${round(price_diff * months_remaining, 2)} owed from member when switching from a yearly to a monthly membership')

        print(
            f'Total cost for change of membership: ${round(cost_of_change, 2)}')

        request.session['cost_of_change'] = cost_of_change

    if member.payment_plan == 'monthly':
        membership_price = member.membership.monthly_price
    elif member.payment_plan == 'yearly':
        membership_price = member.membership.yearly_price

    context = {
        'member': member,
        'membership_price': membership_price,
        'form': form,
    }

    return render(request, 'gym/membership_update.html', context)
