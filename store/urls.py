from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_view, name='store_view'),
    path('<str:product_id>/',
         views.product_detail, name='product_detail'),
    path('delete/<str:product_id>/',
         views.delete_product, name='delete_product'),
    path('edit/<str:product_id>/',
         views.edit_product, name='edit_product'),
]
