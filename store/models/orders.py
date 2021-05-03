from django.db import models 
from .product import Product
from .customer import Customer
import datetime
class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=50,default='')
    payment= models.CharField(max_length=50,default='')
    address = models.CharField(max_length=100,default='')
    zipcode = models.CharField(max_length=10,default='')
    city = models.CharField(max_length=10,default='')
    state = models.CharField(max_length=10,default='')
    country = models.CharField(max_length=10,default='')
    location = models.CharField(max_length=100,default='')
    date= models.DateField(default=datetime.datetime.today)  
      
    
    def placeOrder(self):
        self.save() 