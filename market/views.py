from django.shortcuts import render


def mask_list(request):
    return render(request, 'mask-main.html')


def filters_list(request):
    return render(request, 'filters-main.html')
