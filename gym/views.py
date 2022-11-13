from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


from .models import Gym, GymImage, Membership, Amenity
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from .forms import UpdateMembershipForm, AddImageToGym
from store.models import Product


def all_gyms(request):

    gyms = Gym.objects.all()

    context = {
        'gyms': gyms,
    }

    return render(request, 'gym/all_gyms.html', context)


def gym_details(request, gym_name):

    gym = Gym.objects.get(name=gym_name)
    gym_images = GymImage.objects.filter(gym=gym)
    GOOGLE_MAPS_SECRET_KEY = settings.GOOGLE_MAPS_SECRET_KEY

    context = {
        'gym': gym,
        'gym_images': gym_images,
        'GOOGLE_MAPS_SECRET_KEY': GOOGLE_MAPS_SECRET_KEY,
    }

    return render(request, 'gym/gym.html', context)


def all_memberships(request):
    """Info about all the memberships"""

    memberships = Membership.objects.all()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    else:
        user_profile = request.user

    print(user_profile)
    context = {
        'memberships': memberships,
        'user_profile': user_profile,
    }

    return render(request, 'gym/all_memberships.html', context)


def membership_signup(request, membership_name):
    user_profile = request.user
    membership = Membership.objects.get(name=membership_name)
    gyms = Gym.objects.all()
    form = UserProfileForm()

    if user_profile.is_authenticated:
        user_profile = UserProfile.objects.get(user=user_profile)
        form = UserProfileForm(instance=user_profile)

        if request.method == 'POST':
            rq = request.POST
            requested_membership = Membership.objects.get(
                name=rq['membership'])

            # Check so that the user doesn't have the same or
            # a lower membership
            if user_profile.membership:
                if user_profile.membership.level > requested_membership.level:
                    messages.warning(
                        request, 'You cannot sign up for lower membership than you already have')
                    return redirect(reverse('all_memberships'))

                if user_profile.membership.level == requested_membership.level:
                    messages.warning(
                        request, f'You already have a {requested_membership.name} membership')
                    return redirect(reverse('all_memberships'))

            if rq['payment_plan'] == 'monthly':
                price = requested_membership.monthly_price
            elif rq['payment_plan'] == 'yearly':
                price = requested_membership.yearly_price

            # Create membership checkout session storage
            # with the membership request data
            membership_data = {
                'membership': rq['membership'],
                'payment_plan': rq['payment_plan'],
                'gym': rq['gyms'] if 'gyms' in rq else None,
                'price': float(price),
                'quantity': 1,
            }

            # Save the member profile details
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid:
                form.save()

            # Store the data in session storage and continue to checkout
            request.session['membership_data'] = membership_data
            return redirect(reverse('checkout_view'))

    else:
        if request.method == 'POST':
            rq = request.POST

            email_exist = UserProfile.objects.filter(email=rq['email'])
            if email_exist:
                messages.info(
                    request, "This email is already taken and/or password isn't correct")
                return redirect(reverse(membership_signup, args=[
                    membership_name]))

            # Check if the password matches and login
            if rq['password1'] == rq['password2']:

                user = authenticate(username=rq['email'],
                                    password=rq['password1'])

                # Create User if they don't exist
                if not user:
                    User.objects.create_user(
                        username=rq['email'],
                        email=rq['email'],
                        password=rq['password1'],
                    )
                    user = authenticate(username=rq['email'],
                                        password=rq['password1'])

                login(request, user)
                messages.success(
                    request, f"You are now logged in as {rq['full_name']}.")
                user_profile = UserProfile.objects.get(user=request.user)

                # Save the member profile details
                form = UserProfileForm(request.POST, instance=user_profile)
                if form.is_valid:
                    form.save()

            else:
                # Handle wrong passwords diffrently
                messages.info(
                    request, f"The passwords don't match, please try again!")
                return redirect(reverse('membership_signup', args=[
                    membership_name]))

            requested_membership = Membership.objects.get(
                name=rq['membership'])

            # Check so that the user doesn't have the same
            # or a lower membership
            if user_profile.membership:
                if user_profile.membership.level > requested_membership.level:
                    messages.warning(
                        request, 'You cannot sign up for lower membership than you already have!')
                    return redirect(reverse('all_memberships'))

                if user_profile.membership.level == requested_membership.level:
                    messages.warning(
                        request, f'You already have a {requested_membership.name} membership!')
                    return redirect(reverse('all_memberships'))

            else:
                # Go to membership checkout page
                # Create membership checkout session storage with the
                # membership request data
                if rq['payment_plan'] == 'monthly':
                    price = requested_membership.monthly_price
                elif rq['payment_plan'] == 'yearly':
                    price = requested_membership.monthly_price

                membership_data = {
                    'user_profile_id': user_profile.id,
                    'membership': rq['membership'],
                    'payment_plan': rq['payment_plan'],
                    'gym': rq['gyms'] if 'gyms' in rq else None,
                    'price': float(price),
                    'quantity': 1,
                }

                request.session['membership_data'] = membership_data
                return redirect(reverse('checkout_view'))

    context = {
        'membership': membership,
        'user_profile': user_profile,
        'form': form,
        'gyms': gyms
    }

    return render(request, 'gym/membership_signup.html', context)


def membership_update(request):
    member = UserProfile.objects.get(user=request.user)
    form = UpdateMembershipForm(instance=member)

    cost_of_change = 0
    membership = member.membership
    last_mshp_chg = member.membership_renewed
    mshp_expires = member.membership_expires_on
    months_remaining = round((mshp_expires - last_mshp_chg).days / 30)

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        membership_data = request.session.get('membership_data', {})
        rq = request.POST

        if 'membership' in rq:
            prev_mshp = membership
            new_mshp = Membership.objects.get(level=rq['membership'])
            current_payment_plan = member.payment_plan

            if current_payment_plan == 'yearly':
                # Refund for the months that are left of the memberships since
                # they already paid for the full year
                refund = ((prev_mshp.yearly_price) / 12) * months_remaining

                request.session['membership_data']['refund'] = refund

                cost_of_change += new_mshp.yearly_price - refund
                print(
                    f'Refund ${refund} owed to member when switching from {prev_mshp} membership to a {new_mshp} membership\nTotal membership difference: ${round(cost_of_change, 2)}')
            request.session['membership_data']['membership'] = new_mshp.name

        if 'payment_plan' in rq:
            prev_pp = member.payment_plan
            new_pp = rq['payment_plan']

            if prev_pp != new_pp:
                if prev_pp == 'yearly' and new_pp == 'monthly':
                    monthly_price = membership.monthly_price
                    yearly_price_month_avg = membership.yearly_price / 12
                    price_diff = float(monthly_price) - yearly_price_month_avg

                    request.session[
                        'membership_data'][
                            'payment_plan_change_cost'] = price_diff

                    cost_of_change += price_diff * months_remaining
                    print(
                        f'Extra ${round(price_diff * months_remaining, 2)} owed from member when switching from a yearly to a monthly membership')
            request.session['membership_data']['payment_plan'] = new_pp

        print(
            f'Total cost for change of membership: ${round(cost_of_change, 2)}')

        payment_plan = f"{rq['payment_plan'][0]}/{rq['payment_plan'][0]}"
        membership_product = Product.objects.get(
            name=f'{membership.name} membership {payment_plan}')
        cart[membership_product.id] = 1

        request.session['membership_data']['cost_of_change'] = cost_of_change
        print(request.session['membership_data'])
        request.session['cart'] = cart

    if member.payment_plan == 'monthly':
        membership_price = member.membership.monthly_price
    elif member.payment_plan == 'yearly':
        membership_price = member.membership.yearly_price

    context = {
        'member': member,
        'membership_price': membership_price,
        'form': form,
    }

    return render(request, 'gym/membership_update.html', context)


def is_gym_manager(user):
    return user.groups.filter(name='Gym Manager').exists()


@login_required
@user_passes_test(is_gym_manager)
def gym_edit(request, gym_name):
    gym = Gym.objects.get(name=gym_name)
    amenities = Amenity.objects.all()
    gym_images = GymImage.objects.filter(gym=gym)
    image_form = AddImageToGym()
    GOOGLE_MAPS_SECRET_KEY = settings.GOOGLE_MAPS_SECRET_KEY

    if request.method == "POST":
        rp = request.POST

        gym.address = rp['address']
        gym.email = rp['email']
        gym.phone = rp['phone']
        gym.opening_hours_weekdays = rp['opening_hours_weekdays']
        gym.opening_hours_weekends = rp['opening_hours_weekends']
        gym.closing_hours_weekdays = rp['closing_hours_weekdays']
        gym.closing_hours_weekends = rp['closing_hours_weekends']

        gym.save()
        gym = Gym.objects.get(name=gym_name)

    context = {
        'gym': gym,
        'image_form': image_form,
        'amenities': amenities,
        'gym_images': gym_images,
        'GOOGLE_MAPS_SECRET_KEY': GOOGLE_MAPS_SECRET_KEY,
    }

    return render(request, 'gym/gym_edit.html', context)


@login_required
@user_passes_test(is_gym_manager)
def delete_amenity(request, gym_name, amenity_id):
    gym = Gym.objects.get(name=gym_name)
    amenity = Amenity.objects.get(id=amenity_id)
    gym.amenities.remove(amenity)
    return redirect(reverse('gym_edit', args=[gym_name]))


@login_required
@user_passes_test(is_gym_manager)
def add_amenity(request, gym_name, amenity_id):
    gym = Gym.objects.get(name=gym_name)
    amenity = Amenity.objects.get(id=amenity_id)
    gym.amenities.add(amenity)
    return redirect(reverse('gym_edit', args=[gym_name]))


@login_required
@user_passes_test(is_gym_manager)
def delete_image(request, gym_name, image_id):
    GymImage.objects.get(id=image_id).delete()
    return redirect(reverse('gym_edit', args=[gym_name]))


@login_required
@user_passes_test(is_gym_manager)
def add_image(request, gym_name):
    if request.method == 'POST':
        gym = Gym.objects.get(name=request.POST['gym'])
        form = AddImageToGym(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.gym = gym
            image.save()
    return redirect(reverse('gym_edit', args=[gym_name]))
