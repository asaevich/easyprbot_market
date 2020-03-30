from market.apps import MarketConfig


def appname(request):
    app_label = MarketConfig.name
    return {'app_name': app_label}
