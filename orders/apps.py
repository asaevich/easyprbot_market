from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders'
    verbose_name = 'Заказы и статистика'

    def ready(self):
        # Регистрация сигналов при инициализации приложения
        import orders.signals
