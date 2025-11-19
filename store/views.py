from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models import Product, Category, Customer, Order

class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        
        products = None
        categories = Category.objects.all()
        categoryID = request.GET.get('category')
        
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
            
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'index.html', data)

class Signup(View):
    def get(self, request):
        # Redirect to homepage if already logged in
        if request.session.get('customer'):
            return redirect('homepage')
            
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        error_message = None
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        if not first_name:
            error_message = "First Name Required !!"
        elif len(first_name) < 4:
            error_message = "First Name must be 4 char long or more"
        elif not last_name:
            error_message = "Last Name Required"
        elif not phone:
            error_message = "Phone Number Required"
        elif len(password) < 6:
            error_message = "Password must be 6 char long"
        elif len(email) < 5:
            error_message = "Email must be 5 char long"
        elif customer.isExists():
            error_message = "Email Address Already Registered.."

        if not error_message:
            # Hash password for security
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('login')
        else:
            data = {
                'error': error_message,
                'values': postData
            }
            return render(request, 'signup.html', data)

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

class Login(View):
    return_url = None

    def get(self, request):
        # Redirect to homepage if already logged in as Customer
        if request.session.get('customer'):
            return redirect('homepage')
        
        # Redirect to admin dashboard if logged in as Admin
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('/admin')

        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 1. TRY CUSTOMER LOGIN
        customer = Customer.get_customer_by_email(email)
        error_message = None
        
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                # Password wrong for customer, but maybe it's an admin?
                pass 

        # 2. TRY ADMIN (DJANGO USER) LOGIN
        # Find Django User by email (since login form sends email, but auth needs username)
        try:
            django_user = User.objects.filter(email=email).first()
            if django_user:
                # Authenticate using the username found from the email
                user = authenticate(username=django_user.username, password=password)
                if user is not None:
                    auth_login(request, user)
                    if user.is_staff or user.is_superuser:
                        return redirect('/admin')
                    else:
                        # If regular Django user (not staff), go home
                        return redirect('homepage')
        except Exception as e:
            pass

        # If both failed
        error_message = 'Email or Password invalid !!'
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

from django.contrib.auth.views import LoginView
from django.urls import reverse

class CustomAdminLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect authenticated users away from the admin login page
            return redirect('homepage')  # or any other page you want to redirect to
        return super().get(request, *args, **kwargs)

class Cart(View):
    def get(self, request):
        # RESTRICTION: Block access if not logged in as Customer
        if not request.session.get('customer'):
             return redirect('login')

        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(
                customer=Customer(id=customer),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()
        
        request.session['cart'] = {}
        return redirect('cart')

class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'orders.html', {'orders': orders})