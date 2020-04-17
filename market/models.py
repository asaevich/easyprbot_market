from django.db import models
from datetime import date
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField('Категория', max_length=50, unique=True,
                            blank=False, null=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Creator(models.Model):
    nickname = models.CharField('Создатель', max_length=50, unique=True,
                                blank=False, null=False)

    class Meta:
        verbose_name = 'Создатель'
        verbose_name_plural = 'Создатели'

    def __str__(self):
        return self.nickname


class Customer(models.Model):
    email = models.EmailField('Покупатель', unique=True,
                              blank=False, null=False)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.email


class Product(models.Model):
    is_enable = models.BooleanField('Отображается', default=True)
    disabled_date = models.DateField('Снят с публикации',
                                     null=True, blank=True)
    name = models.CharField('Название', max_length=50, unique=True,
                            blank=False, null=False)
    description = models.TextField('Описание', max_length=400,
                                   blank=False, null=False)
    price = models.FloatField('Обычная цена', null=False)
    discounted_price = models.FloatField('Цена со скидкой', null=True,
                                         blank=True)
    video_link = models.URLField('Ссылка на видео', null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Категория')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_enable:
            self.disabled_date = None
        else:
            self.disabled_date = date.today()
        super(Product, self).save(*args, **kwargs)

    def get_price(self):
        if self.discounted_price:
            return mark_safe(f'<p>{self.discounted_price} &#8381;</p>')
        else:
            return mark_safe(f'<p>{self.price} &#8381;</p>')
    get_price.short_description = 'Цена'


class ProductPhoto(models.Model):
    photo = models.ImageField('Загрузка фото', upload_to='products/',
                              null=False)
    product = models.ForeignKey(Product, verbose_name='Товар',
                                on_delete=models.PROTECT)


class Mask(Product):
    creator = models.ForeignKey(Creator, verbose_name='Создатель маски',
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Маску'
        verbose_name_plural = 'Маски'


class Filter(Product):
    creator = models.ForeignKey(Creator, verbose_name='Создатель фильтра',
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'


class Order(models.Model):
    number = models.IntegerField('Заказ', primary_key=True)
    products = models.ManyToManyField(Product, verbose_name='Товары')
    customer = models.ForeignKey(Customer, verbose_name='Покупатель',
                                 on_delete=models.PROTECT)
    amount = models.FloatField('Сумма', null=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class SalesStatistic(models.Model):
    author = models.ForeignKey(Creator, verbose_name='Автор',
                               on_delete=models.PROTECT)
    sold = models.IntegerField('Продажи', null=False)
    amount = models.FloatField('Сумма', null=False)
    in_stock = models.IntegerField('Товара в наличии', null=False)

    class Meta:
        verbose_name = 'Статистика продаж'
        verbose_name_plural = 'Статистика продаж'
