from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_gyms, name='all_gyms'),
    path('<str:gym_name>/', views.gym, name='gym'),
]
