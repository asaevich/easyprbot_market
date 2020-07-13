from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from market.models import Product, Creator, Customer, Mask


class Order(models.Model):
    number = models.AutoField(primary_key=True, verbose_name='Номер заказа')
    customer = models.ForeignKey(Customer,
                                 verbose_name='Покупатель',
                                 on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.pk}'

    def get_amount(self):
        return sum(item.price for item in self.items.all())
    get_amount.short_description = 'Сумма'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Товар')
    price = models.FloatField('Обычная цена', null=False)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return ''

    def product_link(self):
        if Mask.objects.filter(pk=self.product.pk).exists():
            url = reverse('admin:market_mask_change', args=(self.product.pk,))
        else:
            url = reverse('admin:market_filter_change',
                          args=(self.product.pk,))
        return mark_safe(f"<a href={url}>{self.product.name}</a>")
    product_link.short_description = 'Товар'


class SalesStatistic(models.Model):
    author = models.ForeignKey(Creator,
                               verbose_name='Автор',
                               on_delete=models.PROTECT)
    sold = models.IntegerField('Продажи', null=False)
    amount = models.FloatField('Сумма', null=False)
    in_stock = models.IntegerField('Товара в наличии', null=False)

    class Meta:
        verbose_name = 'Статистика продаж'
        verbose_name_plural = 'Статистика продаж'
