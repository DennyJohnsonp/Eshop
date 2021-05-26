from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    
    
    def __str__(self):
        return self.first_name
    
    def register(self):
        self.save() 

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        
    def get_customer_by_phone(phone):
        try:
            return Customer.objects.get(phone=phone)
        except:
            return False
 
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
    
    def isNumExists(self):
        if Customer.objects.filter(phone=self.phone):
            return True
        else:
            return False