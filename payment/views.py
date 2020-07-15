import braintree
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, get_object_or_404
from orders.models import Customer, Order, OrderItem
from orders.tasks import order_paid
from cart.cart import Cart


class PaymentProcessView(TemplateView):
    """Представление, отображающее страницу оплаты заказа"""
    template_name = 'payment/process.html'

    def get_context_data(self, *args, **kwargs):
        # Формирование одноразового токена для JavaScript SDK
        client_token = braintree.ClientToken.generate()
        context = {'client_token': client_token}
        return context

    def post(self, request, *args, **kwargs):
        # Получение корзины, сохраненной в сессии
        cart = Cart(request)
        # Получение токена для создания транзакции
        nonce = request.POST.get('payment_method_nonce', None)

        # Создание и сохранение транзакции
        result = braintree.Transaction.sale({
            'amount': f'{cart.get_total_price()}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            customer_email = request.session['customer_email']
            customer = get_object_or_404(Customer, email=customer_email)
            order = Order.objects.create(customer=customer)

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'])

            cart.clear()
            # Добавление асинхронной задачи в очередь Celery
            order_paid.delay(order.pk)
            request.session['order_number'] = order.pk

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')


class PaymentDoneView(TemplateView):
    """Представление, отображающее страницу успешной оплаты заказа"""
    template_name = 'payment/done.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, ** kwargs)
        context['order_number'] = self.request.session['order_number']
        return context


class PaymentCanceledView(TemplateView):
    """Представление, отображающее страницу неудачной оплаты заказа"""
    template_name = 'payment/canceled.html'
