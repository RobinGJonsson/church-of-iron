from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkout_view, name='checkout_view'),
    path('checkout_success/<str:order_number>/',
         views.checkout_success, name='checkout_success'),
]
