from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem, SalesStatistic


@receiver(post_save, sender=OrderItem)
def update_sales_statistic(sender, instance, created, **kwargs):
    """
    Обработчик сигнала, срабатывающего после сохранения объекта модели
    элемента заказа. Обновляет кол-во продаж и сумму продаж в записи
    статистики автора данного товара
    """
    # Если товар был создан, а не изменен
    if created:
        creator = instance.product.creator
        statistic = SalesStatistic.objects.get(author=creator)

        statistic.cash_amount += instance.price
        statistic.sold += 1
        statistic.save()
