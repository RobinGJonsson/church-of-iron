from django.forms import ModelForm
from .models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'membership',
                   'payment_plan', 'membership_renewed')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name...',
            'phone': 'Phone Number...',
            'email': 'Email...',
            'address': 'Address...',
            'apartment_number': 'Apartment Number...',
            'postcode': 'Postal Code...',
            'city': 'City...',
            'county': 'County...'
        }

        self.fields['phone'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'input-item'
            self.fields[field].label = False
