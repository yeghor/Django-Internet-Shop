from django.contrib import admin
from .models import ProductCategory, Product, Order
# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)