from django.shortcuts import render
from gym.models import Gym, Membership


def index(request):
    """A view to return the index page"""

    gyms = Gym.objects.all()
    memberships = Membership.objects.all()

    context = {
        'gyms': gyms,
        'memberships': memberships,
    }

    return render(request, 'home/index.html', context)
