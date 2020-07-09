from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from django.core.exceptions import ValidationError
from os.path import basename
from datetime import date


class Category(models.Model):
    name = models.CharField('Категория',
                            max_length=50, unique=True,
                            blank=False,
                            null=False)
    slug = models.SlugField('Слаг',
                            max_length=50,
                            unique=True)
    super_category = models.ForeignKey('Надкатегория',
                                       on_delete=models.PROTECT,
                                       null=True,
                                       blank=True,)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SuperCategoryМanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryМanager()

    def str(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = 'Надкатегория'
        verbose_name_plural = 'Надкатегории'


class SubCategoryМanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryМanager()

    def str(self):
        return f'{self.super_category.name} - {self.name}'

    class Meta:
        proxy = True
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Creator(models.Model):
    nickname = models.CharField('Создатель',
                                max_length=50,
                                unique=True,
                                blank=False,
                                null=False)

    class Meta:
        verbose_name = 'Создатель'
        verbose_name_plural = 'Создатели'

    def __str__(self):
        return self.nickname


class Customer(models.Model):
    email = models.EmailField('Покупатель',
                              unique=True,
                              blank=False,
                              null=False)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.email


class Product(models.Model):
    is_enable = models.BooleanField('Отображается', default=True)
    disabled_date = models.DateField('Товар снят с публикации',
                                     null=True,
                                     blank=True,
                                     editable=False)
    name = models.CharField('Название',
                            max_length=50,
                            unique=True,
                            blank=False,
                            null=False)
    slug = models.SlugField('Слаг',
                            max_length=50,
                            unique=True)
    description = models.TextField('Описание',
                                   max_length=400,
                                   blank=False,
                                   null=False)
    price = models.FloatField('Обычная цена', null=False)
    discounted_price = models.FloatField('Цена со скидкой',
                                         null=True,
                                         blank=True)
    video_link = models.URLField('Ссылка на видео',
                                 null=True,
                                 blank=True)
    category = models.ManyToManyField(SubCategory, verbose_name='Категория')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_enable:
            self.disabled_date = None
        else:
            self.disabled_date = date.today()
        super(Product, self).save(*args, **kwargs)

    def clean(self):
        if self.price and self.price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        if self.discounted_price and self.discounted_price > self.price:
            raise ValidationError(
                'Цена со скидкой не может быть больше обычной цены')

    def get_price(self):
        if self.discounted_price:
            return mark_safe(f'<p>{self.discounted_price} &#8381;</p>')
        else:
            return mark_safe(f'<p>{self.price} &#8381;</p>')
    get_price.short_description = 'Цена'


class ProductPhoto(models.Model):
    photo = models.ImageField('Загрузка фото',
                              upload_to='products/',
                              null=False,
                              blank=False)
    product = models.ForeignKey(Product,
                                verbose_name='Товар',
                                on_delete=models.PROTECT,
                                related_name='photo')
    is_preview = models.BooleanField('Превью', default=False)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

    def __str__(self):
        return basename(str(self.photo))


class Mask(Product):
    creator = models.ForeignKey(Creator,
                                verbose_name='Создатель маски',
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Маску'
        verbose_name_plural = 'Маски'

    def get_absolute_url(self):
        return reverse('market:mask_detail', args=[self.id, self.slug])


class Filter(Product):
    creator = models.ForeignKey(Creator,
                                verbose_name='Создатель фильтра',
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def get_absolute_url(self):
        return reverse('market:filter_detail', args=[self.id, self.slug])


class Order(models.Model):
    number = models.IntegerField('Заказ', primary_key=True)
    products = models.ManyToManyField(Product, verbose_name='Товары')
    customer = models.ForeignKey(Customer,
                                 verbose_name='Покупатель',
                                 on_delete=models.PROTECT)
    amount = models.FloatField('Сумма', null=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


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
