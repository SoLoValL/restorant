from django.conf import settings
from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    """Промокод на скидку"""

    DISCOUNT_TYPES = [
        ('percent', 'Процент'),
        ('fixed', 'Фиксированная сумма'),
    ]

    code = models.CharField('Код', max_length=50, unique=True)
    description = models.TextField('Описание', blank=True)
    discount_type = models.CharField('Тип скидки', max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField('Значение скидки', max_digits=5, decimal_places=2)
    min_order_amount = models.DecimalField('Мин. сумма заказа', max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField('Активен', default=True)
    usage_limit = models.PositiveIntegerField('Лимит использований', null=True, blank=True)
    used_count = models.PositiveIntegerField('Использовано', default=0)
    valid_from = models.DateTimeField('Действует с')
    valid_until = models.DateTimeField('Действует до')
    applicable_categories = models.ManyToManyField('menu.Category', blank=True, related_name='promo_codes')

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active
            and self.valid_from <= now <= self.valid_until
            and (self.usage_limit is None or self.used_count < self.usage_limit)
        )

    @property
    def remaining_uses(self):
        if self.usage_limit is None:
            return None
        return max(0, self.usage_limit - self.used_count)


class Combo(models.Model):
    """Комбо-набор (набор блюд по сниженной цене)"""

    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField(upload_to='combos/', blank=True)
    price = models.DecimalField('Цена комбо', max_digits=8, decimal_places=2)
    original_price = models.DecimalField('Обычная цена', max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField('Активен', default=True)
    is_available = models.BooleanField('В наличии', default=True)
    order = models.PositiveIntegerField(default=0)
    dishes = models.ManyToManyField('menu.Dish', blank=True, related_name='combos')

    class Meta:
        ordering = ['order']
        verbose_name = 'Комбо'
        verbose_name_plural = 'Комбо'

    def __str__(self):
        return self.name

    @property
    def savings(self):
        if self.original_price:
            return self.original_price - self.price
        return None

    @property
    def savings_percent(self):
        if self.original_price and self.original_price > 0:
            return round(float((self.original_price - self.price) / self.original_price * 100), 1)
        return None
