from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator
from .models import Mask, Filter, Category
from .forms import ProductFilterForm


def product_list(request, product_type_slug, category_slug=None):
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

        if product.discounted_price:
            product.old_price = product.price
            product.price = product.discounted_price

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering[0] == '-':
            products = sorted(
                products, key=lambda product: product.price, reverse=True)
        else:
            products = sorted(products, key=lambda product: product.price)
    else:
        ordering = ''
    filter_form = ProductFilterForm(initial={'ordering': ordering})

    paginator = Paginator(products, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.page(page_num)

    context = {'selected_category': selected_category,
               'categories': categories,
               'products': page.object_list,
               'product_type': product_type_slug,
               'pick_class': css_class,
               'page': page,
               'filter_form': filter_form}

    return render(request, 'market/product-list.html', context)


def product_detail(request, product_type_slug, category_slug, product_pk):
    selected_category = None

    if product_type_slug == 'mask':
        product = get_object_or_404(Mask, pk=product_pk)
        products = Mask.objects.filter(is_available=True)
    elif product_type_slug == 'filter':
        product = get_object_or_404(Filter, pk=product_pk)
        products = Filter.objects.filter(is_available=True)
    else:
        raise Http404('Страница не найдена')

    product.images = product.photos.all()
    if product.discounted_price:
        product.old_price = product.price
        product.price = product.discounted_price

    if category_slug != 'all':
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    for p in products:
        p.preview = product.photos.filter(is_preview=True)[0].photo

        if p.discounted_price:
            p.old_price = product.price
            p.price = product.discounted_price

    paginator = Paginator(products, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.page(page_num)

    context = {'selected_category': selected_category,
               'products': page.object_list,
               'product': product,
               'product_type': product_type_slug,
               'page': page}

    return render(request, 'market/product-detail.html', context)


def order_product(request):
    return render(request, 'market/order-product.html')
