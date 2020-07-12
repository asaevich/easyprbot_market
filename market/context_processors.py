from market.apps import MarketConfig


def market_context_processor(request):
    context = {}
    context['all'] = ''
    context['app_name'] = MarketConfig.name

    if 'ordering' in request.GET:
        ordering = request.GET['ordering']

        if ordering:
            context['ordering'] = '?ordering=' + ordering
            context['all'] = context['ordering']

    if 'page' in request.GET:
        page = request.GET['page']

        if page != '1':
            if context.get('all'):
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page

    return context
