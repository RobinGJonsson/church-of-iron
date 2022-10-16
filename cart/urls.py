from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('<str:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('adjust/<str:item_id>/', views.adjust_cart, name='adjust_cart'),
    path('remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
