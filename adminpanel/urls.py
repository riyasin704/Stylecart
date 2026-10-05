from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('products/', views.products, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/', views.categories, name='categories'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),

    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'), 
]