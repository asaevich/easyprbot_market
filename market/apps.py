from django.apps import AppConfig


class MarketConfig(AppConfig):
    name = 'market'
    verbose_name = '@easyprbot'

    def ready(self):
        import market.signals
