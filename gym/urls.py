from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_gyms, name='all_gyms'),
    path('memberships/', views.all_memberships, name='all_memberships'),
    path('membership-signup/<str:membership_name>/',
         views.membership_signup, name='membership_signup'),
    path('membership-update/',
         views.membership_update, name='membership_update'),
    path('<str:gym_name>/', views.gym_details, name='gym_details'),
    path('<str:gym_name>/edit/', views.gym_edit, name='gym_edit'),
    path('<str:gym_name>/delete-amenity/<str:amenity_id>/',
         views.delete_amenity, name='delete_amenity'),
    path('<str:gym_name>/delete-image/<str:image_id>/',
         views.delete_image, name='delete_image'),
    path('<str:gym_name>/add-amenity/<str:amenity_id>/',
         views.add_amenity, name='add_amenity'),
    path('<str:gym_name>/add-image/',
         views.add_image, name='add_image'),
]
