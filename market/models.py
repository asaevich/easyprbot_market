from django.db import models


class Mask(models.Model):
    is_enable = models.BooleanField('Включена ли', default=True)
    name = models.CharField('Название', max_length=50,
                            unique=True, blank=False, null=False)
    description = models.TextField('Описание', max_length=400,
                                   blank=False, null=False)
    price = models.FloatField('Обычная цена', null=False)
    discounted_price = models.FloatField('Цена со скидкой', null=True)
    video_link = models.URLField('Ссылка на видео', null=True)
    photo = models.ImageField('Загрузка фото', upload_to='masks/', null=False)
    category = models.ManyToManyField('Category', verbose_name='Категория')
    creator = models.ForeignKey('Creator', on_delete=models.PROTECT,
                                verbose_name='Создатель маски')

    class Meta:
        verbose_name = 'Маска'
        verbose_name_plural = 'Маски'

    def __str__(self):
        return self.name


class Category(models.Model):
    pass


class Creator(models.Model):
    pass
