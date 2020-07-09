"""easyprbot_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url('mask/', views.mask_list, name='mask_list'),
    url('mask/<slug:category_slug>/', views.mask_list,
        name='mask_list_by_category'),
    url('mask/<int:id>/<slug:slug>/', views.mask_detail, name='mask_detail'),
    url('filter/', views.filter_list, name='filter_list'),
    url('filter/<slug:category_slug>/', views.filter_list,
        name='filter_list_by_category'),
    url('filter/<int:id>/<slug:slug>/', views.filter_detail,
        name='filter_detail'),
]
