
from django.contrib import admin
from django.urls import path
from .views import home,login ,signup

urlpatterns = [
    path('', home.index,name='index'),
    path('gallery',home.gallery,name='gallery'),
    path('cart',home.Cart.as_view(),name='cart'),
    path('cart/signup',signup.Signup.as_view(),name='signup'),
    path('cart/login',login.Login.as_view(),name='login'),
    path('cart2',home.cart2,name='cart2'),
    path('orders',home.orders,name='orders'),
]
