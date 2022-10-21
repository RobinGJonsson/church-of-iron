from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone',
                  'address', 'apartment_number',
                  'city', 'postcode',
                  'county',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name...',
            'email': 'Email...',
            'phone': 'Phone Number...',
            'postcode': 'Postal Code...',
            'address': 'Address...',
            'apartment_number': 'Apartment Number...',
            'city': 'City...',
            'county': 'County...',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs = {
                'placeholder': placeholder,
                'class': 'stripe-style-input',
            }

            self.fields[field].label = False
