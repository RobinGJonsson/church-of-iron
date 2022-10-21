from django.contrib import admin
from .models import Gym, GymImage, Amenity, Membership


admin.site.register(Gym)
admin.site.register(GymImage)
admin.site.register(Amenity)
admin.site.register(Membership)
