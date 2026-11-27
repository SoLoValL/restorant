from django.db import models

ZONE_CHOICES = [
    ('main_hall', 'Основной зал'),
    ('terrace', 'Терраса'),
    ('vip', 'VIP-зона'),
    ('window', 'У окон'),
    ('bar', 'У бара'),
]


class Table(models.Model):
    number = models.PositiveIntegerField('Номер стола', unique=True)
    capacity = models.PositiveIntegerField('Вместимость')
    zone = models.CharField(
        'Зона', max_length=20, choices=ZONE_CHOICES, default='main_hall'
    )
    svg_x = models.PositiveIntegerField('Позиция X на карте', default=0)
    svg_y = models.PositiveIntegerField('Позиция Y на карте', default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Стол №{self.number} ({self.capacity} чел.) — {self.get_zone_display}'


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]

    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField(blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    guests_count = models.PositiveIntegerField('Количество гостей')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.date} {self.time}'
