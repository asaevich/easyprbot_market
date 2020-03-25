from django.contrib.postgres.fields import ArrayField
from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=50, unique=True,
                            blank=False, null=False)


class Creator(models.Model):
    nickname = models.CharField('Создатель', max_length=50, unique=True,
                                blank=False, null=False)


class Customer(models.Model):
    email = models.EmailField('Покупатель', unique=True,
                              blank=False, null=False)


class Mask(models.Model):
    is_enable = models.BooleanField('Доступна ли', default=True)
    name = models.CharField('Название', max_length=50,
                            unique=True, blank=False, null=False)
    description = models.TextField('Описание', max_length=400,
                                   blank=False, null=False)
    price = models.FloatField('Обычная цена', null=False)
    discounted_price = models.FloatField('Цена со скидкой', null=True)
    video_link = models.URLField('Ссылка на видео', null=True)
    photo = models.ImageField('Загрузка фото', upload_to='masks/', null=False)
    category = models.ManyToManyField(Category)
    creator = models.ForeignKey(Creator, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Маска'
        verbose_name_plural = 'Маски'

    def __str__(self):
        return self.name


class Filter(models.Model):
    is_enable = models.BooleanField('Доступен ли', default=True)
    name = models.CharField('Название', max_length=50,
                            unique=True, blank=False, null=False)
    description = models.TextField('Описание', max_length=400,
                                   blank=False, null=False)
    price = models.FloatField('Обычная цена', null=False)
    discounted_price = models.FloatField('Цена со скидкой', null=True)
    video_link = models.URLField('Ссылка на видео', null=True)
    photo = models.ImageField(
        'Загрузка фото', upload_to='filters/', null=False)
    category = models.ManyToManyField(Category)
    creator = models.ForeignKey(Creator, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.IntegerField('Заказ', primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    sum = models.FloatField('Сумма', null=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class SalesStatistic(models.Model):
    author = models.ForeignKey(Creator, on_delete=models.PROTECT)
    sold = models.ArrayField(
        models.ForeignKey()
    )
    amount = models.FloatField('Сумма', null=False)
    in_stock = models.IntegerField('Товара в наличии', null=False)

    class Meta:
        verbose_name = 'Статистика продаж'
        verbose_name_plural = 'Статистика продаж'
