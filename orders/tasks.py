from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_paid(order_pk):
    """Задача отправки email-уведомлений при успешном оформлении заказа"""
    order = Order.objects.get(pk=order_pk)
    subject = f'@Easyprbot. Заказ №{order.pk}'
    products = ''

    for item in order.items.all():
        products += f'{item.product.name},'

    message = f'Ваш заказ №{order.pk} был успешно принят.' \
              + f'Список товаров: {products}'
    mail_sent = send_mail(subject,
                          message,
                          'admin@easyprbot.com',
                          [order.customer.email])
    return mail_sent
