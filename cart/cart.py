from django.conf import settings
from market.models import Product


class Cart(object):
    """Класс корзины покупателя"""

    def __init__(self, request):
        """Инициализация объекта корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product):
        """Добавление товара в корзину"""
        product_id = str(product.id)

        if product_id not in self.cart:
            if product.discounted_price:
                self.cart[product_id] = {
                    'price': str(product.discounted_price)}
            else:
                self.cart[product_id] = {'price': str(product.price)}

        self.save()

    def save(self):
        """Сохранение корзины"""
        # Помечаем сессию, как измененную
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def get_total_price(self):
        """Получение общей стоимости товаров в корзине"""
        return sum(float(item['price']) for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Проходим по товарам корзины и получаем соответствующие
        объекты Product
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            product.preview = product.photos.filter(is_preview=True)[0].photo

            if product.discounted_price:
                product.old_price = product.price
                product.price = product.discounted_price

            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = float(item['price'])
            yield item

    def __len__(self):
        """Возвращает кол-во товаров в корзине"""
        return len(self.cart)
