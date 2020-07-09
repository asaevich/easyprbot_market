from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Mask, Filter, Category


def mask_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    masks = Mask.objects.filter(is_enable=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        masks = masks.filter(category=category)

    return render(request, 'mask-list.html',
                  {'category': category,
                   'categories': categories,
                   'products': masks})


def filter_list(request, slug=None):
    return render(request, 'filters-main.html')


def mask_detail(request, id, slug):
    pass


def filter_detail(request, id, slug):
    pass
