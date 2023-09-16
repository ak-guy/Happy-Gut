from django.urls import path
from . import views

urlpatterns = [
    # register user and vendor
    path('registerUser', views.registerUser, name='registerUser'),
    path('registerVendor', views.registerVendor, name='registerVendor'),

    # login, logout and dashboard
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('custdashboard/', views.custdashboard, name='custdashboard'),
    path('venddashboard/', views.venddashboard, name='venddashboard')
]