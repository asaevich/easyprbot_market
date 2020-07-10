from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from .models import Mask, Filter, Category


def product_list(request, product_type_slug, category_slug=None):
    context = {}
    selected_category = None
    categories = Category.objects.all()

    if product_type_slug == 'mask':
        products = Mask.objects.filter(is_available=True)
        css_class = 'first'
    elif product_type_slug == 'filter':
        products = Filter.objects.filter(is_available=True)
        css_class = 'second'
    else:
        raise Http404('Страница не найдена')

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    for product in products:
        product.preview = product.photos.filter(is_preview=True)[0].photo

    paginator = Paginator(products, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'selected_category': selected_category,
               'categories': categories,
               'products': page.object_list,
               'product_type': product_type_slug,
               'pick_class': css_class,
               'page': page}

    return render(request, 'product-list.html', context)


def product_detail(request, product_type_slug, id, product_slug):
    pass


def order_product(request):
    return render(request, 'order-product.html')
