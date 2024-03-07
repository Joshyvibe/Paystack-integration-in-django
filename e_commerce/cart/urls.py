from django.urls import path
from cart.views import add_to_cart, cart, update_cart

urlpatterns = [
    path('cart', cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
]