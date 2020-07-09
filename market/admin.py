from django.contrib import admin
from django.conf import settings
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe

from market.models import (Mask, Filter, SalesStatistic, Order, Creator,
                           SubCategory, Customer, ProductPhoto)


admin.site.register(Creator)
admin.site.register(Customer)
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


@admin.register(SubCategory)
class CategoryAdmin(CustomModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Mask, Filter)
class ProductAdmin(CustomModelAdmin):
    list_display = ('name', 'creator', 'get_price', 'is_enable')
    inlines = [ProductPhotoInline, ]
    filter_horizontal = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('is_enable', 'name', 'slug', 'description', 'price',
                       'discounted_price', 'video_link')
        }),
        ('Поля ниже не отображаются в карточке', {
            'fields': ('category', 'creator')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ProductAdmin, self).get_fieldsets(request, obj)

        if obj and obj.disabled_date:
            fieldsets = (
                (None, {
                    'fields': ('is_enable', 'disabled_date', 'name', 'slug',
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

    def get_field_queryset(self, db, db_field, request):
        # Bahaviour for your field
        if db_field.name == 'category':
            return db_field.remote_field.model.filter(creator=request.user)
        # Default behaviour unchanged
        return super(OrderAdmin, self).get_field_queryset(db, db_field, request)


@admin.register(Order)
class OrderAdmin(CustomModelAdmin):
    list_display = ('number', 'customer', 'amount')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SalesStatistic)
class SalesStatisticAdmin(CustomModelAdmin):
    list_display = ('author', 'sold', 'amount', 'in_stock')
    list_display_links = None
    readonly_fields = ('author', 'sold', 'amount', 'in_stock')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
