from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Membership(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    monthly_price = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def yearly_price(self):
        return int(round(((float(self.month_price) * 12) * 0.9), 0))

    def __str__(self):
        return self.name


class Member(models.Model):

    PAYMENT_FREQ = (
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    )

    member = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)
    payment_plan = models.CharField(max_length=50,
                                    choices=PAYMENT_FREQ,
                                    blank=True)
    member_since = models.DateTimeField(auto_now_add=True, null=True)

    # ! Update from view when membership is renewed
    membership_renewed = models.DateTimeField()

    @property
    def membership_expires_on(self):
        """Returns the membership expiration date"""

        print(self.payment_plan)
        if self.payment_plan == 'monthly':
            time_to_expiration = timedelta(days=30)
        elif self.payment_plan == 'yearly':
            time_to_expiration = timedelta(days=365)
        else:
            return 'No active membership'

        return (self.membership_renewed + time_to_expiration)

    def __str__(self):
        return self.member.username


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
    email = models.EmailField(max_length=254, null=True)
    coordinates_long = models.CharField(max_length=50, null=True)
    coordinates_lat = models.CharField(max_length=50, null=True)
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
