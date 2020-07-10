from market.apps import MarketConfig


def market_context_processor(request):
    context = {}
    context['app_name'] = MarketConfig.name

    if 'page' in request.GET:
        page = request.GET['page']

        if page != '1':
            if context.get('all'):
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page

    return context
