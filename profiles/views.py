from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm
from .models import UserProfile
from checkout.models import Order


# @login_required
def profile(request):

    member = UserProfile.objects.get(user=request.user)
    membership_price = None
    order_history = Order.objects.filter(user_profile=member)

    if member.payment_plan == 'monthly':
        membership_price = member.membership.monthly_price
    elif member.payment_plan == 'yearly':
        membership_price = member.membership.yearly_price

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=member)
        if form.is_valid:
            form.save()
            messages.success(request, 'member Updated Successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=member)

    context = {
        'form': form,
        'member': member,
        'membership_price': membership_price,
        'order_history': order_history,
    }

    return render(request, 'profiles/profile.html', context)
