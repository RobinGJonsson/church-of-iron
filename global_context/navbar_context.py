from gym.models import Gym, Membership
from store.models import Category


def navbar_context(request):

    gyms = Gym.objects.all()
    memberships = Membership.objects.all()
    categories = Category.objects.all()

    cheapest_price = 'memberships.get(name="Bronze").monthly_price'

    context = {
        'gyms': gyms,
        'memberships': memberships,
        'categories': categories,
        'cheapest_price': cheapest_price,
    }

    return context
