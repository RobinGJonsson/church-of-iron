from email.policy import default
from operator import truediv
from pyexpat import model
from tabnanny import verbose
from tokenize import blank_re
from django.db import models


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50)

    def __str__(self):
        return self.friendly_name


class Product(models.Model):

    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True)
    description = models.TextField()
    reviews = models.TextField(null=True, blank=True)
    has_size = models.BooleanField()
    inventory = models.IntegerField()
    delivery = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
