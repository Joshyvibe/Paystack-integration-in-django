from django.urls import path
from . import views
from product.views import product

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('shop/<slug:slug>', product, name='product'),  
   
]
