from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from market.models import Product
from .cart import Cart
from orders.forms import OrderCreateForm
from orders.models import Customer


def cart_add(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_pk)

    product.preview = product.photos.filter(is_preview=True)[0].photo

    if product.discounted_price:
        product.old_price = product.price
        product.price = product.discounted_price

    cart.add(product)

    return redirect('cart:cart_detail')


def cart_remove(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            customer_email = form.cleaned_data['customer_email']

            if not Customer.objects.filter(email=customer_email).exists():
                Customer.objects.create(email=customer_email)

            request.session['customer_email'] = customer_email
            return redirect(reverse('payment:process'))

    order_form = OrderCreateForm()
    return render(request,
                  'cart/cart_detail.html',
                  {'cart': cart, 'order_form': order_form})
