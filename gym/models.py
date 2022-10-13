from django.db import models
from profiles.models import UserProfile
from datetime import timedelta


class Membership(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    month_price = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def year_price(self):
        return (float(self.month_price) * 12) * 0.9

    def __str__(self):
        return self.name


class Member(models.Model):

    PAYMENT_FREQ = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True, blank=True)
    payment_plan = models.CharField(max_length=50,
                                    choices=PAYMENT_FREQ,
                                    blank=True)
    member_since = models.DateTimeField(auto_now_add=True, null=True)
    membership_renewed = models.DateTimeField(auto_now=True, null=True)

    @property
    def membership_expires_on(self):
        """Returns the membership expiration date"""

        print(self.payment_plan)
        if self.payment_plan == 'mothly':
            time_to_expiration = timedelta(days=30)
        elif self.payment_plan == 'yearly':
            time_to_expiration = timedelta(days=365)
        else:
            print('No active memebrship')
            return 'No active membership'

        print(self.membership_renewed + time_to_expiration)

        return (self.membership_renewed + time_to_expiration)

    def __str__(self):
        return self.member.user.username


class Amenity(models.Model):
    class Meta:
        verbose_name_plural = 'Amenites'

    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50)
    icon = models.CharField(max_length=200)

    def __str__(self):
        return self.friendly_name


class Gym(models.Model):

    members = models.ManyToManyField(Member, blank=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    description = models.TextField()
    main_image = models.ImageField()
    opening_hours_weekdays = models.TimeField()
    opening_hours_weekends = models.TimeField()
    closing_hours_weekdays = models.TimeField()
    closing_hours_weekends = models.TimeField()
    amenities = models.ManyToManyField(Amenity)

    def __str__(self):
        return self.name


class GymImage(models.Model):

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    alt = models.CharField(max_length=50)

    def __str__(self):
        return self.gym.name
