from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_gyms, name='all_gyms'),
    path('memberships/', views.all_memberships, name='all_memberships'),
    path('<str:gym_name>/', views.gym, name='gym'),
    path('<str:membership_name> membership/',
         views.membership, name='membership'),
]
