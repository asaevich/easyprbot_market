import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Customer, Order, OrderItem
from orders.tasks import order_paid
from cart.cart import Cart


def payment_process(request):
    cart = Cart(request)

    if request.method == 'POST':
        # Получение токена для создания транзакции.
        nonce = request.POST.get('payment_method_nonce', None)

        # Создание и сохранение транзакции.
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
            order_paid.delay(order.pk)
            request.session['order_number'] = order.pk

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Формирование одноразового токена для JavaScript SDK.
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'client_token': client_token})


def payment_done(request):
    order_number = request.session['order_number']
    return render(request, 'payment/done.html', {'order_number': order_number})


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
