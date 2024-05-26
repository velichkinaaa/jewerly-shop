from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'user': request.user if request.user.id else None
    }
    return render(request, 'index.html', context)


def product_view(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product-details.html', context)


@login_required(login_url='login')
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        user_p_ids = cart.product_ids.split()
    except Cart.DoesNotExist:
        user_p_ids = []
        cart = None
    cart_produtcs = []
    for p_id in user_p_ids:
        cart_produtcs.append(Product.objects.get(id=int(p_id)))
    context = {
        'cart_products': cart_produtcs,
        'cart': cart
    }
    return render(request, 'cart.html', context)


def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':
        order = Order(
            cart=cart,
            company_name=request.POST.get('company'),
            country=request.POST.get('country'),
            address=request.POST.get('street_address'),
            town=request.POST.get('city'),
            zip_code=request.POST.get('zipCode'),
            phone=request.POST.get('phone_number'),
            comment=request.POST.get('comment')
        )
        order.save()
        cart.delete()
        return render(request, 'success.html')
    context = {
        'cart': cart
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def dark(request):
    if request.session['dark']:
        request.session['dark'] = False
    else:
        request.session['dark'] = True
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def font(request):
    if request.session['font']:
        request.session['font'] = False
    else:
        request.session['font'] = True
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        try:
            cart = Cart.objects.get(user=user)
            cart.product_ids += f' {str(product_id)}'
            cart.save()
        except Cart.DoesNotExist:
            n_cart = Cart(
                user=user,
                product_ids=str(product_id)
            )
            n_cart.save()
        return redirect('product', product_id)


@login_required(login_url='login')
def remove_from_cart(request, id):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        print(cart.product_ids)
        cart.product_ids = cart.product_ids\
            .replace(f' {id} ', ' ')\
            .replace(f'{id}', '')\
            .replace(f' {id}', '')
        print(cart.product_ids)
        cart.save()
    except Cart.DoesNotExist:
        return redirect('cart')
    return redirect('cart')


def search(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        products = Product.objects.filter(title__contains=str(query).upper())
        context = {
            'products': products,
        }
        return render(request, 'index.html', context)


def sign_up(request):
    if request.method == 'POST':
        user = User(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('email'),
            password=make_password(request.POST.get('password'))
        )
        try:
            user.save()
            return redirect('login')
        except:
            return 'Error'
    return render(request, 'sign_up.html')


def log_in(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            request.session['dark'] = False
            request.session['font'] = False
            return redirect('index')
        else:
            return redirect('login')
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('login')
