from django.forms import ModelForm

from profiles.models import UserProfile


class UpdateMembershipForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('membership', 'payment_plan')
