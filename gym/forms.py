from django.forms import ModelForm

from profiles.models import UserProfile
from .models import GymImage


class UpdateMembershipForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('membership', 'payment_plan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'list-group-item'


class AddImageToGym(ModelForm):

    class Meta:
        model = GymImage
        fields = ('image', 'alt',)

        labels = {
            "alt": ("Image Description"),
        }
