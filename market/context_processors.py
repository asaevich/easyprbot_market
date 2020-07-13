from market.apps import MarketConfig


def market_context_processor(request):
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
