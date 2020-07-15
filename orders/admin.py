from django.contrib import admin
from market.admin import CustomModelAdmin
from .models import Customer, Order, OrderItem, SalesStatistic


admin.site.register(Customer)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    exclude = ('product', 'price')
    readonly_fields = ('product_link',)


@admin.register(Order)
class OrderAdmin(CustomModelAdmin):
    list_display = ('number', 'customer', 'get_amount')
    readonly_fields = ('number', 'customer', 'get_amount')
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(SalesStatistic)
class SalesStatisticAdmin(CustomModelAdmin):
    list_display = ('author', 'sold', 'cash_amount', 'product_amount')
    list_display_links = None
    readonly_fields = ('author', 'sold', 'cash_amount', 'product_amount')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
