from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View


def index(request):
    return render(request, 'index.html')


def gallery(request):
    return render(request, 'gallery.html')

class Cart(View):
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:    
                cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print("CART",request.session['cart'])
        return redirect('cart')
    
    def get(self, request):
        products =None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'cart.html', data)


def cart2(request):
    prds = Product.get_all_products()
    return render(request, 'cart2.html',{'products':prds})


def orders(request):
    return render(request, 'orders/orders.html')
