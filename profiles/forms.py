from django.forms import ModelForm
from gym.models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member
        exclude = ('member', 'membership',
                   'payment_plan', 'membership_renewed')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name...',
            'last_name': 'Last Name...',
            'phone': 'Phone Number...',
            'city': 'City...',
            'address': 'Address...',
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
