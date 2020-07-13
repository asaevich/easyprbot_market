from django.shortcuts import render, redirect, get_object_or_404
from market.models import Product
from .cart import Cart


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
    return render(request, 'cart/cart_detail.html', {'cart': cart})
