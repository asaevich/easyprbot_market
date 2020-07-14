from django.shortcuts import render, redirect, get_object_or_404
from market.models import Product
from .cart import Cart
from orders.tasks import order_paid
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
from market.models import Customer


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

            if Customer.objects.filter(email=customer_email).exists():
                customer = Customer.objects.get(email=customer_email)
            else:
                customer = Customer.objects.create(email=customer_email)

            order = Order.objects.create(customer=customer)
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'])
            cart.clear()
            order_paid.delay(order.pk)

            return render(request,
                          'orders/successful-payment.html',
                          {'order': order})

    order_form = OrderCreateForm()
    return render(request,
                  'cart/cart_detail.html',
                  {'cart': cart, 'order_form': order_form})
