from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm
from .models import UserProfile
from checkout.models import Order


@login_required
def profile(request):

    user = get_object_or_404(UserProfile, user=request.user)
    membership_price = None
    order_history = Order.objects.filter(user_profile=user)

    if user.payment_plan == 'monthly':
        membership_price = user.membership.monthly_price
    elif user.payment_plan == 'yearly':
        membership_price = user.membership.yearly_price

    if request.method == 'POST':
        print(user)
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            messages.success(request, 'user updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        print(user.address)
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'user': user,
        'membership_price': membership_price,
        'order_history': order_history,
    }

    return render(request, 'profiles/profile.html', context)
