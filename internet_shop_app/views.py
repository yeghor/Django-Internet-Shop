from django.shortcuts import render, redirect
from .models import ProductCategory, Product, Order
from django.contrib.auth.decorators import login_required
from django.http import Http404
from cart.cart import Cart
from internet_shop.settings import CART_SESSION_ID
from cart.forms import CartForm
import hashlib
import datetime
from random import randint
from .forms import OrderForm

def del_cart(request):
    if CART_SESSION_ID in request.session:
        del request.session[CART_SESSION_ID]


def index(request):
    cart = Cart(request) 
    total_price = cart.get_total_price()
    context = {
        'cart': cart,
        'total_price': total_price
    }
    return render(request, 'internet_shop_app/index.html', context)

def error_404(request, exception):
    return render(request, 'internet_shop_app/error_404.html', status=404)

def error_page(request):
    return render(request, 'internet_shop_app/error_page.html')

def stock_error_page(request):
    return render(request, 'internet_shop_app/stock_error_page.html')

def error_500(request):
    return render(request, 'internet_shop_app/error_500.html')

def check_order_owner(request, order_id):
    order = Order.objects.get(order_id=order_id)
    if order.owner != request.user:
        raise Http404

def products_categories_page(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    cart = Cart(request) 
    total_price = cart.get_total_price()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart,
        'total_price': total_price,
    }
    return render(request, 'internet_shop_app/products_categories_page.html', context)

def products_page(request, category_id):
    category = ProductCategory.objects.get(id=category_id)
    products = Product.objects.filter(category_id=category_id)
    cart = Cart(request) 
    total_price = cart.get_total_price()
    context = {
        'products': products,
        'category': category,
        'cart': cart,
        'total_price': total_price,
    }
    return render(request, 'internet_shop_app/products_page.html', context)

@login_required
def product_page(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    
    #form code    
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            temp_quantity = cart.cart.get(str(product.id), {}).get('quantity')
            if temp_quantity == None:
                temp_quantity = 0

            temp_quantity = temp_quantity + quantity
            if temp_quantity > product.stock:
                return redirect('internet_shop_app:stock_error_page')

            cart.add(product=product, quantity=quantity)        
    else:
        form = CartForm()

    total_price = cart.get_total_price()
    context = {
        'product': product,
        'form': form,
        'cart': cart,
        'total_price': total_price,
    }
    return render(request, 'internet_shop_app/product_page.html', context)

@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('internet_shop_app:products_categories_page')

@login_required
def order_form_page(request):
    cart = Cart(request)    
    total_price = cart.get_total_price()    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(form.errors)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            post_office = form.cleaned_data['post_office']
            special_wishes = form.cleaned_data['special_wishes']
            payment_method = form.cleaned_data['payment_method']
            delivery_date = form.cleaned_data['delivery_date']

            hashed_id, timestamp = get_hashed_id()

            order_item_list, order_data, order_id = make_order_obj(cart, first_name, last_name, email, phone_number, address, post_office, special_wishes, payment_method, delivery_date, hashed_id, timestamp)
            #logic for checking available stock
            for item in cart:
                item_id = item['id']
                product = Product.objects.get(id=item_id)

                if item['quantity'] <= product.stock:
                    product.stock -= item['quantity']
                    product.save()
                else:
                    return redirect('internet_shop_app:error_page')
            #
            put_order_in_db(request, total_price=total_price, order_item_list=order_item_list, order_data=order_data, order_id=order_id)
            cart.clear()
            return redirect('internet_shop_app:order_confirmation_page', order_id=order_data['order_id'])
    else:
        form = OrderForm()
        cart.status = 'checkout'

    context = {
        'form': form,
        'total_price': total_price,
        'cart': cart,
    }
    return render(request, 'internet_shop_app/order_form_page.html', context)

def get_hashed_id():
    timestamp = datetime.datetime.now()
    unique_string = f"{timestamp}-{randint(1, 1000000)}"
    hashed_id = hashlib.sha256(unique_string.encode()).hexdigest()[:10]   
    return hashed_id, timestamp

def put_order_in_db(request, total_price, order_item_list, order_data, order_id):
    order = Order(total_price_for_cart=total_price, order_item_list=order_item_list, order_data=order_data, order_id=order_id, owner=request.user)
    order.save()

def make_order_obj(cart, first_name, last_name, email, phone_number, address, post_office, special_wishes, payment_method, delivery_date, hashed_id, timestamp):
    order_item_list = []
    for item in cart:
        product = Product.objects.get(id=item['id'])
        order_item = {
            'order_id': str(hashed_id),
            'product_id': product.id,
            'product_name': product.name,
            'total_price_for_product': item['total_price'],
            'quantity': item['quantity'],
        }

        order_item_list.append(order_item)

    order_data = {
            'datetime': str(timestamp),
            'order_id': str(hashed_id),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': str(phone_number),
            'address': address,
            'post_office': post_office,
            'special_wishes': special_wishes,
            'payment_method': payment_method,
            'delivery_date': str(delivery_date),
    }
    return order_item_list, order_data, hashed_id

@login_required
def order_confirmation_page(request, order_id):
    check_order_owner(request, order_id)
    order = Order.objects.get(order_id=order_id)
    context = {
        'order_data': order.order_data,
        'order_item_list': order.order_item_list,
    }

    return render(request, 'internet_shop_app/order_confirmation_page.html', context)