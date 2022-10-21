from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User

from .models import UserProfile

from datetime import datetime


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
        print('Created UserProfile')


@receiver(pre_save, sender=UserProfile)
def update_membership_renewed(sender, instance, **kwargs):
    saved_instance = UserProfile.objects.get(id=instance.id)

    # If memebership has changed
    if saved_instance.membership != instance.membership:
        instance.membership_renewed = datetime.now().date()
