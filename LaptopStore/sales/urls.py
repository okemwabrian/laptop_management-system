from django.urls import path
from . import views

urlpatterns = [
    path('', views.laptop_list, name='laptop_list'),
    path('laptop/<int:laptop_id>/', views.laptop_detail, name='laptop_detail'),
    path('sales-history/', views.sales_history, name='sales_history'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
