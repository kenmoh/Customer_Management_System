from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account', views.account_settings, name='account'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('register', views.register, name='register'),
    path('customer/<str:customer_id>', views.customer, name='customer'),
    path('product', views.product, name='product'),
    path('create_order/<str:customer_id>', views.create_order, name='create_order'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('update_customer/<str:customer_id>', views.update_customer, name='update_customer'),
    path('delete_customer/<str:customer_id>', views.delete_customer, name='delete_customer'),
    path('update_order/<str:order_id>', views.update_order, name='update_order'),
    path('delete_order/<str:order_id>', views.delete_order, name='delete_order'),
]