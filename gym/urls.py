from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_gyms, name='all_gyms'),
    path('memberships/', views.all_memberships, name='all_memberships'),
    path('membership-signup/<str:membership_name>/',
         views.membership_signup, name='membership_signup'),
    path('membership-checkout/', views.membership_checkout,
         name='membership_checkout'),
    path('membership-update/',
         views.membership_update, name='membership_update'),
    path('<str:gym_name>/', views.gym_details, name='gym_details'),
]
