from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Cart(models.Model):
    """Корзина пользователя"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True,
    )
    session_key = models.CharField('Ключ сессии', max_length=40, blank=True, default='')
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        user_str = self.user.username if self.user else self.session_key or 'anonymous'
        return f'Корзина: {user_str}'

    @property
    def total_price(self):
        return sum(item.total for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Товар в корзине"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey('menu.Dish', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Количество', default=1, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['dish__name']
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'
        unique_together = ('cart', 'dish')

    def __str__(self):
        return f'{self.dish.name} x {self.quantity}'

    @property
    def total(self):
        return self.dish.price * self.quantity
