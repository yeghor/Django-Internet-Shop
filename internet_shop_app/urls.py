from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'internet_shop_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('products_categories_page/', views.products_categories_page, name='products_categories_page'),
    path('products_page/<int:category_id>/', views.products_page, name='products_page'),
    path('product_page/<int:product_id>/', views.product_page, name='product_page'),
    path('product_page/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_form_page/', views.order_form_page, name='order_form_page'),
    path('order_confirmation_page/<str:order_id>/', views.order_confirmation_page, name='order_confirmation_page'),
    path('error_404/', views.error_404, name='error_404'),
    path('error_page/', views.error_page, name='error_page'),
    path('error_500/', views.error_500, name='error_500'),
    path('stock_error_page/', views.stock_error_page, name='stock_error_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)