from django.urls import path
from . import views
from payment.views import verify_payment


urlpatterns = [
    path('order', views.start_order, name='start_order'),
    path('verify_payment<str:ref>/', verify_payment, name='verify_payment')
   
   
]
