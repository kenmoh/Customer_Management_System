from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from .models import Product, Customer, Order
from .forms import OrderForm, CustomerForm, UserCreateForm
from .filters import OrderFilter
from .decorators import unauthenticated_user


@unauthenticated_user
def register(request):
    # User Registration function
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for {username} was created successfully !')
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def user_login(request):
    # User Login Function
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, f'Incorrect username or password')
    context = {}
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required(login_url='user_login')
def home(request):
    # This function displays the dashboard
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'customers': customers,
               'total_customers': total_customers,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending
               }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='user_login')
def create_customer(request):
    # This function creates a new customer
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/create_customer.html', context)


@login_required(login_url='user_login')
def update_customer(request, customer_id):
    # This is used to update a single customer by it id
    customer = Customer.objects.get(id=customer_id)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/create_customer.html', context)


@login_required(login_url='user_login')
def delete_customer(request, customer_id):
    # To delete a customer from the database
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    context = {'customer': customer}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='user_login')
def customer(request, customer_id):
    # Displays a single customer dashboard
    customer = Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    order_count = orders.count()
    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs
    context = {'customer': customer,
               'orders': orders,
               'order_count': order_count,
               'order_filter': order_filter,
               }
    return render(request, 'accounts/customer.html', context)


def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
            form = CustomerForm(request.POST, request.FILES, instance=request.user.customer)
            if form.is_valid():
                form.save()
            messages.success(request, 'Profile Updated successfully !')
    context = {'form': form}
    return render(request, 'accounts/account_setting.html', context)
    

@login_required(login_url='user_login')
def product(request):
    # To get all products from the database
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='user_login')
def create_order(request, customer_id):
    # Create an order for a customer
    order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    customer = Customer.objects.get(id=customer_id)
    # form = OrderForm(initial={'customer': customer})
    form = order_form_set(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        form = order_form_set(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form, 'customer': customer}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='user_login')
def update_order(request, order_id):
    # Updates a single order by it's id
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='user_login')
def delete_order(request, order_id):
    # Delete an order from the database
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/dashboard.html', context)