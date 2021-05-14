
from django.contrib import admin
from django.urls import path
from .views import home, login, signup, bag, checkout,particular, orders
from .middlewares.auth import auth_middleware
from .middlewares.checkauth import auth_check_middleware

urlpatterns = [
    path('', home.index,name='index'),
    path('gallery',home.gallery,name='gallery'),
    path('cart',home.Cart.as_view(),name='cart'),
    path('cart/signup',signup.Signup.as_view(),name='signup'),
    path('cart/login',login.Login.as_view(),name='login'),
    path('cart/logout',login.logout,name='logout'),
    path('cart/bag',bag.Bag.as_view(),name='bag'),
    path('cart/bag/checkout',auth_check_middleware(checkout.CheckOut.as_view()),name='checkout'),
    path('orders',auth_middleware(orders.OrderView.as_view()),name='orders'),
    path('cart/particular/<int:id>/',particular.Particular.as_view(),name='particular'),
    path('orders',home.orders,name='orders'),
]
