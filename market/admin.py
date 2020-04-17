from django.contrib import admin
from django.conf import settings

from market.models import (Mask, Filter, SalesStatistic, Order, Creator,
                           Category, Customer, ProductPhoto)


admin.site.register(Category)
admin.site.register(Creator)
admin.site.register(Customer)
admin.site.register(ProductPhoto)

admin.site.site_header = 'Панель администратора'
admin.site.index_title = 'Администрирование'


class CustomModelAdmin(admin.ModelAdmin):
    list_per_page = settings.LIST_PER_PAGE


@admin.register(Mask, Filter)
class ProductAdmin(CustomModelAdmin):
    list_display = ('name', 'creator', 'get_price', 'is_enable')

    def get_exclude(self, request, obj=None):
        exclude = super(ProductAdmin, self).get_exclude(request, obj)

        if obj:
            if not obj.disabled_date:
                exclude = ('disabled_date',)

        return exclude

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(
            ProductAdmin, self).get_readonly_fields(request, obj)

        if obj:
            if obj.disabled_date:
                readonly_fields = ('disabled_date',)

        return readonly_fields


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
