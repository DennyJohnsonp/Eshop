
from django.contrib import admin
from django.urls import path
from .views import home, login, signup, bag, checkout

urlpatterns = [
    path('', home.index,name='index'),
    path('gallery',home.gallery,name='gallery'),
    path('cart',home.Cart.as_view(),name='cart'),
    path('cart/signup',signup.Signup.as_view(),name='signup'),
    path('cart/login',login.Login.as_view(),name='login'),
    path('cart/logout',login.logout,name='logout'),
    path('cart/bag',bag.Bag.as_view(),name='bag'),
    path('cart/bag/checkout',checkout.CheckOut.as_view(),name='checkout'),
    path('cart/particular/<int:id>/',home.productdetail,name='particular'),
    path('orders',home.orders,name='orders'),
]
