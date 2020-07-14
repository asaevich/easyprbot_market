from django.db import models
from django.utils.html import mark_safe
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

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


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


class Product(models.Model):
    is_available = models.BooleanField('Отображается', default=True)
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
    category = models.ManyToManyField(Category, verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_available:
            self.disabled_date = None
        else:
            self.disabled_date = date.today()
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for photo in self.photos.all():
            photo.delete()
        super().delete(*args, **kwargs)

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
                                on_delete=models.CASCADE,
                                related_name='photos')
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


class Filter(Product):
    creator = models.ForeignKey(Creator,
                                verbose_name='Создатель фильтра',
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'
