from django.shortcuts import render, redirect
from django.contrib.auth.hashers import  check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from store.models.orders import Order
from django.views import View


class CheckOut(View):
    def get(self, request):
        return render(request, 'checkout.html')
    def post(self , request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        payment = request.POST.get('payment')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        location = request.POST.get('location')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        product= Product.get_product_by_id(list(cart.keys()))
        print(firstname,lastname,phone,payment,address,zipcode,city,state,country,location,customer,cart,product)
        for product in product:
            order = Order(customer= Customer(id= customer), product= product,price=product.price,firstname=firstname,lastname=lastname,phone=phone,payment=payment,address=address,zipcode=zipcode,city=city,state=state,country=country,location=location, quantity=cart.get(str(product.id)))
            order.placeOrder()
        request.session['cart']={}
        return redirect("orders")