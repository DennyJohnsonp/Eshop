from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.views import View
from django.contrib.auth import logout

class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url =request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        customer = Customer.get_customer_by_email(email)
        print(customer)
        phone = request.POST.get('email')
        print(phone)
        customerp = Customer.get_customer_by_phone(phone)
        print(customerp)
        error_message = None
        if customer:
            flag = check_password(password , customer.password)
            if flag:
                request.session['customer']= customer.id
            
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('cart')
            else:
                error_message = "!!! Invalid User ID or Password!!!"
        else:
            error_message = "!!! Invalid User ID or Password!!!"
        if customerp:
            flag = check_password(password , customerp.password)
            if flag:
                request.session['customer']= customerp.id
            
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('cart')
            else:
                error_message = "!!! Invalid User ID or Password!!!"
        else:
            error_message = "!!! Invalid User ID or Password!!!"
        return render(request,'login.html',{'error':error_message})

def logout(request):
    request.session.clear()
    print(request.session)
    return redirect('login')