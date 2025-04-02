from django import forms
from phonenumber_field.formfields import PhoneNumberField

class OrderForm(forms.Form):
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    email = forms.EmailField(label='E-mail', required=True)
    phone_number = PhoneNumberField(label='Phone number', required=True)
    address = forms.CharField(label='Address', required=False)
    post_office = forms.CharField(label='Post office (City, № - Nova Poshta office number)', required=True)
    special_wishes = forms.CharField(label='Have any special wishes? Let us know', required=False)
    payment_method = forms.ChoiceField(label='Payment Method', choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash_on_delivery', 'Cash on Delivery')])
    delivery_date = forms.DateField(label='Preferred Delivery Date', required=False, widget=forms.SelectDateWidget)
