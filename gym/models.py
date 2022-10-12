from pyexpat import model
from tabnanny import verbose
from django.db import models


class Amenity(models.Model):
    class Meta:
        verbose_name_plural = 'Amenites'

    name = models. models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50)
    icon = models.CharField(max_length=200)


class GymImage(models.Model):

    image = models.ImageField()
    alt = models.CharField(max_length=50)


class Gym(models.Model):

    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    description = models.TextField()
    main_image = models.ImageField()
    images = models.ImageField()
    opening_hours_weekdays = models.TimeField()
    opening_hours_weekends = models.TimeField()
    closing_hours_weekdays = models.TimeField()
    closing_hours_weekends = models.TimeField()
    amenities = models.ManyToManyField(Amenity)
