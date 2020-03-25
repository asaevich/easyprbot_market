from django.contrib import admin

from market.models import Mask, Filter, SalesStatistic, Orders, Creator, \
    Category, Customer

admin.site.register(Mask)
admin.site.register(Filter)
admin.site.register(Orders)
admin.site.register(SalesStatistic)
admin.site.register(Category)
admin.site.register(Creator)
admin.site.register(Customer)
