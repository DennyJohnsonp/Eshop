from django.shortcuts import render, redirect
from django.contrib.auth.hashers import  check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from store.models.orders import Order
from django.views import View
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import phonenumbers
from phonenumbers import geocoder




class CheckOut(View):
    def get(self, request):
        id=request.session.get('customer')
        phone=Customer.objects.get(id=int(id)).phone
        print(phone)
        firstname=Customer.objects.get(id=int(id)).first_name
        print(firstname)
        lastname=Customer.objects.get(id=int(id)).last_name
        print(lastname)
        value={
            'phone':phone,
            'firstname':firstname,
            'lastname':lastname,
        }
        data ={
                'values': value,
        }
        return render(request, 'checkout.html',data)
    
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
        for product in product:
            order = Order(customer= Customer(id= customer), product= product,price=product.price,firstname=firstname,lastname=lastname,phone=phone,payment=payment,address=address,zipcode=zipcode,city=city,state=state,country=country,location=location, quantity=cart.get(str(product.id)))
            order.placeOrder()
        customer= request.session.get('customer')
        orders= Order.get_orders_by_customer(customer)
        order = request.session.get('order')
        ids = list(request.session.get('cart').keys())
        products= Product.get_product_by_id(ids)
        cart=request.session['cart']
        customer = Order(firstname=firstname,lastname=lastname,phone=phone,payment=payment,address=address,zipcode=zipcode,city=city,state=state,country=country,location=location,)
        error_message = None
        error_message = self.validateCustomer(customer)
        value = {
                'firstname':firstname,
                'lastname':lastname,
                'phone':phone,
                'payment':payment,
                'address':address,
                'zipcode':zipcode,
                'city':city,
                'state':state,
                'location':location,
                'country':country,
            }
        if (not error_message):
            context = {
                'name':firstname+lastname,
                'phone':phone,
                'payment':payment,
                'address':address,
                'zipcode':zipcode,
                'city':city,
                'state':state,
                'location':location,
                'orders':orders,
                'products':products,
                'cart':cart,
            }
            template=render_to_string('../../store/templates/ordersmail.html',context)
            id=request.session.get('customer')
            mail=Customer.objects.get(id=int(id)).email
            print(mail)
            email=EmailMultiAlternatives(
                    'Thank You For The Order ',
                    template,
                    settings.EMAIL_HOST_USER,
                    [mail],
                )
            email.attach_alternative(template,"text/html")
            email.send()    
            request.session['cart']={}
            return redirect('orders')
            
        else:
            country=geocoder.description_for_number(phonenumbers.parse(customer.phone), "en")
            data ={
                'error': error_message,
                'values': value,
                'country':country
            }
            return render(request, 'checkout.html',data)

    def validateCustomer(self, customer):
        error_message = None;
       
        if (not customer.firstname):
            error_message = "!!! First Name Required !!!"
        elif len(customer.firstname) < 4:
            error_message = "!!! First Name Must Be Greater Than 4 Characters or More !!! "
        elif (not customer.firstname.isalpha()):
                error_message = "!!!Only Characters Are Allowed For First Name !!!"
        elif (not customer.lastname):
            error_message = "!!! Last Name Required !!!"
        elif len(customer.lastname) < 4:
            error_message = "!!! Last Name Must Be Greater Than 4 Characters or More !!! "
        elif (not customer.lastname.isalpha()):
                error_message = "!!!Only Characters Are Allowed For Last Name !!!"
        elif (not customer.phone):
            error_message = "!!! Phone Number Required !!!"
        elif len(customer.phone) < 13:
            error_message = "!!! Phone Number Must Not Be Lesser Than 13 Characters  !!! "
        elif len(customer.phone) > 13:
            error_message = "!!! Phone Number Must Not  Be Greater Than 13 Characters  !!! "
        elif (not customer.payment):
            error_message = "!!! Payment Method Required !!!"
        elif (not customer.address):
                error_message = "!!! Address Detail Required !!!"
        elif len(customer.address) < 10:
            error_message = "!!!Address  Must Be Greater Than 10 Characters or More !!! "
        elif (not customer.zipcode):
                error_message = "!!! Zipcode Detail  Required !!!"
        elif len(customer.zipcode)>6:
            error_message = "!!!Zipcode  Must Be Equal To 6 Characters Not More !!! "
        elif len(customer.zipcode)<6:
            error_message = "!!!Zipcode  Must Be Equal To 6 Characters Not Less !!! "
        elif (not customer.zipcode.isnumeric()):
                error_message = "!!! Zipcode Not Valid!!!"
        elif (not customer.city):
                error_message = "!!! City Detail Required !!!"
        elif len(customer.city) < 4:
            error_message = "!!!City Must Be Greater Than 4 Characters or More !!! "
        elif (not customer.city.isalpha()):
                error_message = "!!! Invalid City Details !!!"
        elif (not customer.state):
                error_message = "!!!State Detail Required !!!"
        elif len(customer.state) < 4:
            error_message = "!!!State  Must Not Be Greater Than 4 Characters or More !!! "
        elif (not customer.state.isalpha()):
                error_message = "!!! Invalid State Details !!!"
        elif (not customer.country):
                error_message = "!!!Country Detail Required Select From Below!!!"
        elif (not customer.country.isalpha()):
                error_message = "!!! Invalid Country Details !!!"
        elif (not customer.location):
                error_message = "!!!Location Detail Required Share Location Or Copy and Paste Link!!!"
        elif  (customer.phone):    
            message=phonenumbers.is_valid_number(phonenumbers.parse(customer.phone))
            if not message==True:
                error_message="Please Enter a Valid Number "
        return error_message


 