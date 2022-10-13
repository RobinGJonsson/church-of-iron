from django.shortcuts import render
from .models import Gym, GymImage


def all_gyms(request):

    gyms = Gym.objects.all()

    context = {
        'gyms': gyms,
    }

    return render(request, 'gym/all_gyms.html', context)


def gym(request, gym_name):

    gym = Gym.objects.get(name=gym_name)
    gym_images = GymImage.objects.filter(gym=gym)

    context = {
        'gym': gym,
        'gym_images': gym_images,
    }

    return render(request, 'gym/gym.html', context)
