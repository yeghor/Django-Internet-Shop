from django.urls import path, include
from . import views
import django.contrib.auth.urls

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]