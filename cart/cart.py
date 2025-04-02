from decimal import Decimal
from django.conf import settings
from internet_shop_app.models import Product
from internet_shop.settings import CART_SESSION_ID
from django.shortcuts import render, redirect
class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        self.status = 'in_progress'

    def add(self, product, quantity=1, update_quantity=False):
        str_id = str(product.id)
        if str_id not in self.cart.keys():
            self.cart[str_id] = {
                'quantity': 0,
                'price': str(product.price),
                }
        if update_quantity:
            self.cart[str_id]['quantity'] = quantity
        else:
            self.cart[str_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        if str(product.id) in self.cart.keys():
            del self.cart[str(product.id)]
            self.save()

    def __iter__(self):
        
        for item_key, item in self.cart.items():
            item_key_id_int = int(item_key)
            product = Product.objects.get(id=item_key_id_int)
            item['name'] = product.name
            item['total_price'] = str(Decimal(item['price']) * item['quantity'])
            item['id'] = product.id
            yield item

    def __len__(self):
        return sum(product['quantity'] for product in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(product['price']) * product['quantity'] for product in self.cart.values())
    
    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True