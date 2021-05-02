from django.shortcuts import render, redirect
from django.contrib.auth.hashers import  check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View


class CheckOut(View):
    def get(self, request):
        return render(request, 'checkout.html')
    def post(self , request):
        print(request.POST)
        return redirect('bag.html')