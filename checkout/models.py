import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from store.models import Product
from gym.models import Member


class Order(models.Model):
    @property
    def order_number(self):
        return uuid.uuid4().hex.upper()
    #! Change user profile to work for non memebers
    user_profile = models.ForeignKey(Member, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(
        max_length=40, null=False, blank=False, default='')
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def calc_costs(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.order_items.aggregate(
            Sum('item_subtotal'))
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            sdp = settings.STANDARD_DELIVERY_PERCENTAGE
            self.delivery_cost = self.order_total * sdp / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='order_items')
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True,
                                    blank=True)  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'
