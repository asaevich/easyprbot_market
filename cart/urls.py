from django.urls import path
from .views import CartAddView, CartRemoveView, CartDetailView

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_pk>/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:product_pk>/', CartRemoveView.as_view(),
         name='cart_remove'),
]
