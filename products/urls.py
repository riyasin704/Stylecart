from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_products, name='category_products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.customer_login, name='login'),
    path('logout/', views.customer_logout, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    
]