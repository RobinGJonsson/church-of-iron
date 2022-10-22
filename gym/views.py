from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from .models import Gym, GymImage, Membership
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


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


def member_signup(request, membership_name):

    membership = Membership.objects.get(name=membership_name)
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(instance=user_profile)
    else:
        user_profile = request.user
        form = UserProfileForm()

    if request.method == 'POST':

        # If user does not have an account create an account
        if not request.user.is_authenticated:
            rq = request.POST

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
                return redirect(reverse('member_signup', args=[membership.name]))

        rq = request.POST
        form_data = {
            'full_name': rq['full_name'],
            'email': rq['email'],
            'phone': rq['phone'],
            'membership': membership,
            'payment_plan': rq['payment_plan'],
        }

        for key, value in form_data.items():
            setattr(user_profile, key, value)
        user_profile.save()
        return redirect('/')

    context = {
        'membership': membership,
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'gym/member_signup.html', context)
