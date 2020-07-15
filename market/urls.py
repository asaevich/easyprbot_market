from django.urls import path
from .views import OrderProductView
from . import views

app_name = 'market'

urlpatterns = [
    path('order-product/', OrderProductView.as_view(), name='order_product'),
    path('<slug:product_type_slug>/', views.product_list, name='product_list'),
    path('<slug:product_type_slug>/<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<slug:product_type_slug>/<slug:category_slug>/<int:product_pk>/',
         views.product_detail, name='product_detail'),
]
