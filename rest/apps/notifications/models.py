from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Уведомления пользователей"""

    NOTIFICATION_TYPES = [
        ('order_created', 'Заказ создан'),
        ('order_confirmed', 'Заказ подтверждён'),
        ('order_cancelled', 'Заказ отменён'),
        ('reservation_confirmed', 'Бронирование подтверждено'),
        ('reservation_cancelled', 'Бронирование отменено'),
        ('points_earned', 'Баллы начислены'),
        ('points_expired', 'Баллы сгорели'),
        ('promo_used', 'Промокод применён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    notification_type = models.CharField('Тип', max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField('Заголовок', max_length=200)
    message = models.TextField('Сообщение')
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.user.username}: {self.title}'
