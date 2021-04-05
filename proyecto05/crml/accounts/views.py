from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .filters import OrderFilter

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():            
            user = form.save()
            username = form.cleaned_data.get('username')

            #Creo un user nuevo asociado al grupo "customer"
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            #Cuando creo un usuario nuevo lo asocio a un Customer
            Customer.objects.create(
                user=user
            )
            messages.success(request, "Account was created for "+username)
            return redirect("login")
    context={'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    print(request.user)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Username or password is incorrect ")
            context={}
            return render(request, 'accounts/login.html', context)
    context={}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    #orders = request.user.customer.order_set.all()
    customers=Customer.objects.filter(user=request.user)
    customer = customers[0]
    orders = customer.order_set.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders}
    context={"orders":orders,
        "total_customers": total_customers,
        "total_orders":total_orders,
        "delivered":delivered,
        "pending":pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context={"orders":orders,
            "customers":customers,
            "total_customers": total_customers,
            "total_orders":total_orders,
            "delivered":delivered,
            "pending":pending}
    return render(request, "accounts/dashboard.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    
    products=Product.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "accounts/products.html", context={"products":page_obj})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request ,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    #customer = Customer.objects.all().filter(id=pk_test)

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {"customer":customer, 
                "orders":orders, 
                "myFilter":myFilter }

    return render(request, "accounts/customer.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context={"form": form}
    return render(request, "accounts/form.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrders(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'note', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet(instance=customer)
    if request.method == "POST":
        formset = orderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')

    context={"formset": formset}
    return render(request, "accounts/form_set.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order=Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={"form": form}
    return render(request, "accounts/form.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order=Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard')
    context={"order": order}
    return render(request, "accounts/delete.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCostumer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context={"form": form}
    return render(request, "accounts/form.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer=Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={"form": form}
    return render(request, "accounts/form.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    customer=Customer.objects.get(id=pk)
    customer.delete()
    return redirect("dashboard")