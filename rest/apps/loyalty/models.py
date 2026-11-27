from django.conf import settings
from django.db import models


class LoyaltyCard(models.Model):
    """Карта лояльности пользователя"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loyalty_card',
    )
    points_balance = models.PositiveIntegerField('Баланс баллов', default=0)
    total_earned = models.PositiveIntegerField('Всего заработано', default=0)
    total_spent = models.PositiveIntegerField('Всего потрачено', default=0)
    level = models.CharField(
        'Уровень',
        max_length=20,
        choices=[
            ('bronze', 'Бронзовый'),
            ('silver', 'Серебряный'),
            ('gold', 'Золотой'),
            ('platinum', 'Платиновый'),
        ],
        default='bronze',
    )
    discount_percent = models.DecimalField('Скидка', max_digits=5, decimal_places=2, default=0)
    registered_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Карта лояльности'
        verbose_name_plural = 'Карты лояльности'

    def __str__(self):
        return f'{self.user.username} — {self.points_balance} баллов'

    def calculate_level(self):
        """Определение уровня по количеству заработанных баллов"""
        if self.total_earned >= 10000:
            level = 'platinum'
            discount = 15
        elif self.total_earned >= 5000:
            level = 'gold'
            discount = 10
        elif self.total_earned >= 1000:
            level = 'silver'
            discount = 5
        else:
            level = 'bronze'
            discount = 0

        if self.level != level:
            self.level = level
            self.discount_percent = discount
            self.save(update_fields=['level', 'discount_percent'])


class PointsHistory(models.Model):
    """История начисления/списания баллов"""

    OPERATIONS = [
        ('earned', 'Начисление'),
        ('spent', 'Списание'),
        ('expired', 'Сгорание'),
        ('bonus', 'Бонус'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='points_history',
    )
    points = models.IntegerField('Баллы')
    operation_type = models.CharField('Тип операции', max_length=20, choices=OPERATIONS)
    description = models.TextField('Описание', blank=True)
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='points_record',
    )
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'История баллов'
        verbose_name_plural = 'История баллов'

    def __str__(self):
        sign = '+' if self.points > 0 else '-'
        return f'{self.user.username}: {sign}{abs(self.points)} ({self.get_operation_type_display()})'
