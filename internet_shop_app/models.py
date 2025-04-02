from django.db import models
from django.contrib.auth.models import User
from django.http import HttpRequest
class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField()
    class Meta:
        verbose_name_plural = 'product  categories'

    def __str__(self):
        return self.title
    

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads', blank=True, null=True)

    def get_actual_stock(self, request: HttpRequest ):
        return None

    def __str__(self):
        if len(self.description) < 50:
            return self.description
        else:
            return self.description[:50]+'...'

class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=20)
    total_price_for_cart = models.DecimalField(max_digits=20, decimal_places=2)    
    order_item_list = models.JSONField()
    order_data = models.JSONField()



