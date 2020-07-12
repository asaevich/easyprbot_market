from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('order-product/', views.order_product, name='order_product'),
    path('<slug:product_type_slug>/', views.product_list, name='product_list'),
    path('<slug:product_type_slug>/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<slug:product_type_slug>/<int:id>/<slug:product_slug>/',
         views.product_detail, name='product_detail'),
]
