from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    readonly_fields = (
        'member_since', 'membership_expires_on', 'membership_renewed',)


admin.site.register(UserProfile, UserProfileAdmin)
