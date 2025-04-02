from django import forms
from cart.cart import Cart

class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=50, label='Quantity')

