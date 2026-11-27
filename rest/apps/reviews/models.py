from django.conf import settings
from django.db import models


class DishReview(models.Model):
    """Отзыв к конкретному блюду"""

    dish = models.ForeignKey('menu.Dish', on_delete=models.CASCADE, related_name='dish_reviews')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='dish_reviews',
        null=True,
        blank=True,
    )
    rating = models.PositiveSmallIntegerField('Оценка')
    text = models.TextField('Текст отзыва', blank=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв к блюду'
        verbose_name_plural = 'Отзывы к блюдам'
        unique_together = ('dish', 'author')

    def __str__(self):
        return f'{self.dish.name} — {self.author} ({self.rating})'


class Review(models.Model):
    RATING_LABELS = [
        ('1', 'Ужасно'),
        ('2', 'Плохо'),
        ('3', 'Нормально'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='reviews',
        null=True,
        blank=True,
    )
    rating = models.PositiveSmallIntegerField('Оценка')
    text = models.TextField('Отзыв')
    is_published = models.BooleanField('Опубликовано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author} ({self.rating})'

    @property
    def rating_label(self):
        labels = dict(self.RATING_LABELS)
        return labels.get(str(self.rating), '')

    @property
    def author_total_reviews(self):
        if self.author:
            return Review.objects.filter(author=self.author, is_published=True).count()
        return 0
