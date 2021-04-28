from django.shortcuts import render, redirect
from django.contrib.auth.hashers import  check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View


class Bag(View):
    
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products= Product.get_product_by_id(ids)
        print(products)
        return render(request, 'bag.html')
