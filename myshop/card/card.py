from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Card:
    def __init__(self, request):
        """
        Инициализаия корзины.
        """
        self.session = request.session
        card = self.session.get(settings.CART_SESSION_ID)
        if not card:
            # сохранить пустую корзину в сеансе
            card = self.session[settings.CART_SESSION_ID] = {}
        self.card = card
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """Добавление товара в корзину"""
        product_id = str(product.id)
        if product_id not in self.card:
            self.card[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.card[product_id]['quantity'] = quantity
        else:
            self.card[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # пометить сеанс как "измененный", чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.card:
            del self.card[product_id]
        self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """

        product_ids = self.card.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        card = self.card.copy()
        for product in products:
            card[str(product.id)]['product'] = product
        for item in card.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """

        return sum(item['quantity'] for item in self.card.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.card.values())

    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
