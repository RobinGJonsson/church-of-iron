from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User

from .models import UserProfile

from datetime import datetime


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=UserProfile)
def update_membership_renewed(sender, instance, **kwargs):

    # Wrap in try block because if the this signal was called when a
    # User was created, the UserProfile does not yet exist because
    # this is pre_save
    # A post_save doesn't know about the previous instance, so it has to be pre_save
    try:
        old_instance = sender.objects.get(id=instance.id)
        payment_plan_changed = old_instance.payment_plan != instance.payment_plan
        membership_changed = old_instance.membership != instance.membership

        if payment_plan_changed or membership_changed:
            instance.membership_renewed = datetime.now()

    except Exception as e:
        print(e, '\nMembership renewed will not be updated from signal because the UserProfile does not exist yet')
