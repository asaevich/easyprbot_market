from django.db.models.signals import post_save, post_delete
from .models import Product
from orders.models import SalesStatistic


def update_statistic_post_save(sender, instance, created, **kwargs):
    """
    Обработчик сигнала, срабатывающего после сохранения объекта модели
    товара. Обновляет кол-во товара в наличие в записи статистики
    автора данного товара
    """
    # Если товар создан впервые и для него включено отображение на сайте
    if created and instance.is_available:
        # Если это первый товар данного автора,
        # то создаем новый объект статистики
        if not SalesStatistic.objects.filter(author=instance.creator).exists():
            statistic = SalesStatistic.objects.create(author=instance.creator,
                                                      sold=0,
                                                      cash_amount=0,
                                                      product_amount=1)
        # Если товар не первый, то объект статистики уже существует
        else:
            statistic = SalesStatistic.objects.get(author=instance.creator)
            statistic.product_amount += 1

        statistic.save()
    # Если товар был изменен, а не создан впервые
    elif not created:
        updated = kwargs['update_fields']

        if updated and 'is_available' in updated:
            # Если поле disabled_date равно None,
            # то для товара только что было включено отображение на сайте
            if not instance.disabled_date:
                # Частный случай: если товар был создан с выключенным
                # отображением на сайте и это единственный товар данного
                # создателя, то объект статистики не был создан, при создании
                # товара и его необходимо добавить
                if not SalesStatistic.objects.filter(
                        author=instance.creator).exists():
                    statistic = SalesStatistic.objects.create(
                        author=instance.creator,
                        sold=0,
                        cash_amount=0,
                        product_amount=1)
                # Если объект статистики уже существовал
                else:
                    statistic = SalesStatistic.objects.get(
                        author=instance.creator)
                    statistic.product_amount += 1
            # Если поле disabled_date не равно None,
            # то для товара только что было выключено отображение на сайте
            else:
                statistic = SalesStatistic.objects.get(author=instance.creator)
                statistic.product_amount -= 1

            statistic.save()


def update_statistic_post_delete(sender, instance, using, **kwargs):
    """
    Обработчик сигнала, срабатывающего после удаления объекта модели
    товара. Обновляет кол-во товара в наличие в записи статистики
    автора данного товара
    """
    if instance.is_available:
        statistic = SalesStatistic.objects.get(author=instance.creator)
        statistic.product_amount -= 1
        statistic.save()


# Коннектим сигналы к каждому наследнику класса Product
for subclass in Product.__subclasses__():
    post_save.connect(update_statistic_post_save, sender=subclass)
    post_delete.connect(update_statistic_post_delete, sender=subclass)
