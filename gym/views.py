from django.shortcuts import render
from .models import Gym, GymImage, Membership, Member


def all_gyms(request):

    gyms = Gym.objects.all()

    context = {
        'gyms': gyms,
    }

    return render(request, 'gym/all_gyms.html', context)


def gym_details(request, gym_name):

    gym = Gym.objects.get(name=gym_name)
    gym_images = GymImage.objects.filter(gym=gym)

    context = {
        'gym': gym,
        'gym_images': gym_images,
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
    member = Member.objects.get(member=request.user)

    context = {
        'membership': membership,
        'member': member,
    }

    return render(request, 'gym/member_signup.html', context)
