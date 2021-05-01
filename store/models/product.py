from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=50) 
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    short_description = models.CharField(max_length=100,default='',null=True)
    more_description = models.CharField(max_length=600,default='',null=True)
    image = models.ImageField(upload_to='uploads/produts/') 
    
    def get_product_by_id(ids):
        return Product.objects.filter(id__in=ids)
    
    def __str__(self):
        return self.name
    
    def get_all_products():
        return Product.objects.all()
    
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()