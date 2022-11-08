from gym.models import Gym, Membership
from store.models import Category
from django.conf import settings


def navbar_context(request):

    gyms = Gym.objects.all()
    memberships = Membership.objects.all()
    categories = Category.objects.all()

    chepest_price = memberships.get(name="Bronze").monthly_price

    GOOGLE_MAPS_SECRET_KEY = settings.GOOGLE_MAPS_SECRET_KEY

    context = {
        'gyms': gyms,
        'memberships': memberships,
        'categories': categories,
        'chepest_price': chepest_price,
    }

    return context
