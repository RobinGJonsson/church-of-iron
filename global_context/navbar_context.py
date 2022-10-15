from gym.models import Gym, Membership
from store.models import Category


def navbar_context(request):

    gyms = Gym.objects.all()
    memberships = Membership.objects.all()
    categories = Category.objects.all()

    context = {
        'gyms': gyms,
        'memberships': memberships,
        'categories': categories,
    }
    return context
