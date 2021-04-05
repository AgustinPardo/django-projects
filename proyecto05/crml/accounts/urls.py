from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="dashboard"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('register/', views.registerPage, name="register"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk_test>', views.customer, name="customer"),

    path('create_orders/<str:pk>', views.createOrders, name="create_orders"),

    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>', views.updateOrder, name="update_order"),
    path('delete/<str:pk>', views.deleteOrder, name="delete_order"),

    path('create_customer/', views.createCostumer, name="create_customer"),
    path('update_customer/<str:pk>', views.updateCustomer, name="update_customer"),
    path('delete_customer/<str:pk>', views.deleteCustomer, name="delete_customer"),
]