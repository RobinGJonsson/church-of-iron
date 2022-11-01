from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item_subtotal',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'created_on',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'user_profile', 'created_on', 'full_name',
              'email', 'phone',
              'postcode', 'city', 'address',
              'apartment_number', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    list_display = ('order_number', 'created_on', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-created_on',)


admin.site.register(Order, OrderAdmin)
