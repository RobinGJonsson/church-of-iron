from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout_view, name='checkout_view'),
    path('checkout-success/',  # Order number or membership number?
         views.checkout_success, name='checkout_success'),

    path('wh/', webhook, name='webhook'),

    # Handles stripe initializtion
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session,
         name='create_checkout_session'),

]
