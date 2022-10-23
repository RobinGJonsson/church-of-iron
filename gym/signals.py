from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Membership
from store.models import Product, Category


@receiver(pre_save, sender=Membership)
def change_membership_product_price(sender, instance, **kwargs):
    """Changes the membership product price when the price of the membbership changes"""

    category = Category.objects.get(name='memberships')
    membership_products = Product.objects.filter(
        category=category, name__icontains=instance.name)

    for membership_product in membership_products:

        if 'm/m' in membership_product.name:
            membership_product.price = instance.monthly_price
            print('changed monthly price ')
        else:
            membership_product.price = instance.yearly_price
            print('changed yearly price ')

    membership_product.save()
