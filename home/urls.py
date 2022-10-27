from django.urls import path
from . import views
from checkout.webhooks import webhook

urlpatterns = [
    path('', views.index, name='home'),
    path('stripe_webhooks/', webhook, name='webhook'),
]
