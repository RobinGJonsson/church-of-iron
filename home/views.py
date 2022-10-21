from django.shortcuts import render, get_object_or_404
from gym.models import Gym, Membership


def index(request):
    """A view to return the index page"""

    gyms = Gym.objects.all()
    memberships = Membership.objects.all()
    gold_membership = get_object_or_404(Membership, name='Gold')

    context = {
        'gyms': gyms,
        'memberships': memberships,
        'gold_membership': gold_membership,
    }

    return render(request, 'home/index.html', context)
