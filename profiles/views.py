from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import MemberForm
from gym.models import Member


@login_required
def profile(request):

    member = get_object_or_404(Member, member=request.user)

    if member.payment_plan == 'monthly':
        membership_price = member.membership.monthly_price
    elif member.payment_plan == 'yearly':
        membership_price = member.membership.yearly_price

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid:
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = MemberForm(instance=member)

    context = {
        'form': form,
        'member': member,
        'membership_price': membership_price,
    }

    return render(request, 'profiles/profile.html', context)
