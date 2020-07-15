from django.contrib import admin
from django.conf import settings
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe
from market.models import (Mask, Filter, Creator,
                           Category, ProductPhoto)

admin.site.register(Creator)
admin.site.register(ProductPhoto)

admin.site.site_header = 'Панель администратора'
admin.site.index_title = 'Администрирование'


class CustomModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []

        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" alt="{file_name}" width="150"'
                f'height="150" style="object-fit: cover; float: right;"/> </a>')

        output.append(super(AdminFileWidget, self).render(
            name, value, attrs, renderer))
        return mark_safe(u''.join(output))


class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }

    def get_min_num(self, request, obj=None, **kwargs):
        return 1

    def get_max_num(self, request, obj=None, **kwargs):
        return 7


@admin.register(Mask, Filter)
class ProductAdmin(CustomModelAdmin):
    list_display = ('name', 'creator', 'get_price', 'is_available')
    inlines = [ProductPhotoInline, ]
    filter_horizontal = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('is_available', 'name', 'slug', 'description', 'price',
                       'discounted_price', 'video_link')
        }),
        ('Поля ниже не отображаются в карточке', {
            'fields': ('category', 'creator')
        }),
    )

    def save_model(self, request, obj, form, change):
        update_fields = []

        if change:
            if form.initial['is_available'] != form.cleaned_data['is_available']:
                update_fields.append('is_available')

        obj.save(update_fields=update_fields)
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ProductAdmin, self).get_fieldsets(request, obj)

        if obj and obj.disabled_date:
            fieldsets = (
                (None, {
                    'fields': ('is_available', 'disabled_date', 'name', 'slug',
                               'description', 'price', 'discounted_price',
                               'video_link')
                }),
                ('Поля ниже не отображаются в карточке', {
                    'fields': ('category', 'creator')
                }),
            )

        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(
            ProductAdmin, self).get_readonly_fields(request, obj)

        if obj:
            if obj.disabled_date:
                readonly_fields = ('disabled_date',)

        return readonly_fields


@admin.register(Category)
class CategoryAdmin(CustomModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
