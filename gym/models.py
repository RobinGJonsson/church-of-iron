from django.db import models
from profiles.models import UserProfile


class Membership(models.Model):

    name = models.CharField(max_length=50)
    level = models.IntegerField(null=True)
    description = models.TextField()
    monthly_price = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def yearly_price(self):
        return int(round(((float(self.monthly_price) * 12) * 0.9), 0))

    def __str__(self):
        return self.name


class Amenity(models.Model):
    class Meta:
        verbose_name_plural = 'Amenites'

    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50)
    icon = models.CharField(max_length=200)

    def __str__(self):
        return self.friendly_name


class Gym(models.Model):

    members = models.ManyToManyField(
        UserProfile, blank=True, related_name='gym')
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
