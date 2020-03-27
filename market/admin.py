from django.contrib import admin
from django.utils.html import mark_safe

from market.models import (Mask, Filter, SalesStatistic, Order, Creator,
                           Category, Customer, ProductPhoto)


admin.site.register(Category)
admin.site.register(Creator)
admin.site.register(Customer)
admin.site.register(ProductPhoto)

admin.site.site_header = 'Панель администратора'
admin.site.index_title = 'Администрирование'


@admin.register(Mask)
class MaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'get_price', 'is_enable')

    def get_price(self, obj):
        if obj.discounted_price:
            return mark_safe(f'<p>{obj.discounted_price} &#8381;</p>')
        else:
            return mark_safe(f'<p>{obj.price} &#8381;</p>')

    get_price.short_description = 'Цена'


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'get_price', 'is_enable')

    def get_price(self, obj):
        if obj.discounted_price:
            return mark_safe(f'<p>{obj.discounted_price} &#8381;</p>')
        else:
            return mark_safe(f'<p>{obj.price} &#8381;</p>')

    get_price.short_description = 'Цена'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'customer', 'amount')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SalesStatistic)
class SalesStatisticAdmin(admin.ModelAdmin):
    list_display = ('author', 'sold', 'amount', 'in_stock')
    list_display_links = None
    readonly_fields = ('author', 'sold', 'amount', 'in_stock')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
