from django.contrib import admin

from market.models import Mask, Filter, SalesStatistic, Order, Creator, \
    Category, Customer, ProductPhoto

admin.site.register(Mask)
admin.site.register(Filter)
admin.site.register(Order)
admin.site.register(SalesStatistic)
admin.site.register(Category)
admin.site.register(Creator)
admin.site.register(Customer)
admin.site.register(ProductPhoto)
