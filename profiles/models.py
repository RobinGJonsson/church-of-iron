from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta


class UserProfile(models.Model):
    PAYMENT_FREQ = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    apartment_number = models.IntegerField(null=True, blank=True)
    postcode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)

    membership = models.ForeignKey(
        "gym.Membership", on_delete=models.CASCADE, null=True, blank=True)
    payment_plan = models.CharField(max_length=50,
                                    choices=PAYMENT_FREQ,
                                    blank=True)
    member_since = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)

    membership_renewed = models.DateTimeField(
        null=True, blank=True, editable=False)

    @property
    def membership_expires_on(self):
        """Returns the membership expiration date"""

        if self.payment_plan == 'monthly':
            time_to_expiration = timedelta(days=30)
        elif self.payment_plan == 'yearly':
            time_to_expiration = timedelta(days=365)
        else:
            return 'No active membership'

        return (self.membership_renewed + time_to_expiration)

    def __str__(self):
        return self.user.email
