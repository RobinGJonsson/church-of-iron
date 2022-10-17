from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone',
                  'street_address1', 'street_address2',
                  'city', 'postcode',
                  'county',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name...',
            'email': 'Email...',
            'phone': 'Phone Number...',
            'street_address1': 'Street Address 1...',
            'street_address2': 'Street Address 2...',
            'city': 'City',
            'county': 'County',
        }

        self.fields['full_name'].widget.attr['autofocus'] = True
        for field in self.fields:
            if field.required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            field.widget.attr['placeholders'] = placeholder
            field.widget.attr['class'] = 'input-item'
            field.label = False
