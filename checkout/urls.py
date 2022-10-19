from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout_view, name='checkout_view'),
    path('checkout_success/<str:order_number>/',
         views.checkout_success, name='checkout_success'),
    path('wh/', webhook, name='webhook'),
]
