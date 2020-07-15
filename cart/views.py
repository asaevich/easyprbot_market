from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from market.models import Product
from .cart import Cart
from orders.forms import OrderCreateForm
from orders.models import Customer


class CartDetailView(FormView):
    """Представление, отображающее страницу корзины"""
    template_name = 'cart/cart_detail.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('payment:process')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        customer_email = form.cleaned_data['customer_email']

        if not Customer.objects.filter(email=customer_email).exists():
            Customer.objects.create(email=customer_email)

        self.request.session['customer_email'] = customer_email

        return super().form_valid(form)


class CartAddView(RedirectView):
    """
    Представление, совершающее добавление товара в корзину
    и переход на страницу корзины
    """

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=kwargs['product_pk'])

        product.preview = product.photos.filter(is_preview=True)[0].photo

        if product.discounted_price:
            product.old_price = product.price
            product.price = product.discounted_price

        cart.add(product)

        return redirect('cart:cart_detail')


class CartRemoveView(RedirectView):
    """
    Представление, совершающее удаление товара из корзины
    и переход на страницу корзины
    """

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=kwargs['product_pk'])
        cart.remove(product)

        return redirect('cart:cart_detail')
