from datetime import datetime

from django.db import models


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Живая музыка'),
        ('masterclass', 'Мастер-класс'),
        ('thursday', 'Тематический вечер'),
        ('holiday', 'Праздник'),
        ('business', 'Бизнес-ланч'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Название', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
    full_description = models.TextField('Полное описание', blank=True, help_text='Подробное описание события')
    image = models.ImageField('Изображение', upload_to='events/', blank=True)
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    end_time = models.TimeField('Окончание', blank=True, null=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, default=0)
    location = models.CharField('Место проведения', max_length=200, blank=True)
    organizer = models.CharField('Организатор', max_length=200, blank=True)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='other')
    max_guests = models.PositiveIntegerField('Макс. гостей', blank=True, null=True)
    is_active = models.BooleanField('Активно', default=True)
    is_featured = models.BooleanField('Рекомендуемое', default=False)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.title

    @property
    def bookings_count(self):
        return self.bookings.count()

    @property
    def available_spots(self):
        if self.max_guests:
            return max(0, self.max_guests - self.bookings_count)
        return None

    @property
    def duration_minutes(self):
        if self.time and self.end_time:
            diff = (
                datetime.combine(datetime.today(), self.end_time) -
                datetime.combine(datetime.today(), self.time)
            ).seconds // 60
            return diff
        return 0


class EventBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email', blank=True)
    guests_count = models.PositiveIntegerField('Количество гостей', default=1)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20, default='pending')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование события'
        verbose_name_plural = 'Бронирования событий'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.event}'
