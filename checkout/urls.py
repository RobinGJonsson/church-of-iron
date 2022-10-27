from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout_view, name='checkout_view'),
    path('checkout_success/<str:order_number>/',
         views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),

    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
]
