from market.apps import MarketConfig


def market(request):
    """
    Контекстный процессор, добавляющий в каждый контекст запроса
    GET-параметры для корректного отображения страниц, а также
    имя приложения market для отображения в админ. панеле
     """
    context = {}
    context['parameters'] = ''
    context['app_name'] = MarketConfig.name

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering:
            context['ordering'] = '?ordering=' + ordering
            context['parameters'] = context['ordering']

    if 'page' in request.GET:
        page = request.GET['page']

        if page != '1':
            if context.get('parameters'):
                context['parameters'] += '&page=' + page
            else:
                context['parameters'] = '?page=' + page

    return context
