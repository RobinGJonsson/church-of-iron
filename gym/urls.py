from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_gyms, name='all_gyms'),
    path('memberships/', views.all_memberships, name='all_memberships'),
    path('<str:gym_name>/', views.gym_details, name='gym_details'),
    path('membership/<str:membership_name>/',
         views.membership, name='membership'),
    path('membersignup/<str:membership_name>/',
         views.member_signup, name='member_signup'),
]
