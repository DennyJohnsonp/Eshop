from django.shortcuts import render, redirect
from django.contrib.auth.hashers import  make_password, check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Signup(View):
    
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        value = {
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'email': email,
        }
        error_message = None
        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email, password=password)
        error_message = self.validateCustomer(customer)
        if (not error_message):
            customer.password = make_password(customer.password)
            customer.register()
            template=render_to_string('../../store/templates/welcomemail.html',{'name':customer.first_name})
            email=EmailMultiAlternatives(
                'You Have Registered Successfully To Lucky Digital Studio',
                template,
                settings.EMAIL_HOST_USER,
                [customer.email],
            )
            email.attach_alternative(template,"text/html")
            email.send()
            return redirect("cart")
        else:
            data ={
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html',data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "!!! First Name Required !!!"
        elif len(customer.first_name) < 4:
            error_message = "!!! First Name Must Be Greater Than 4 Characters or More !!! "
        elif (not customer.last_name):
            error_message = "!!! Last Name Required !!!"
        elif len(customer.last_name) < 4:
            error_message = "!!! Last Name Must Be Greater Than 4 Characters or More !!! "
        elif (not customer.phone):
            error_message = "!!! Phone Number Required !!!"
        elif len(customer.phone) < 10:
            error_message = "!!! Phone Number Must Be Greater Than 10 Characters or More !!! "
        elif (not customer.password):
            error_message = "!!! Password Required !!!"
        elif len(customer.last_name) < 6:
            error_message = "!!! Password Must Be Greater Than 6 Characters or More !!! "
        elif customer.isExists():
            error_message = "!!!Email Address Already Registered!!!"
        return error_message

 