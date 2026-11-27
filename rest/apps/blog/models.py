from django.conf import settings
from django.db import models


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('kitchen', 'Кухня'),
        ('news', 'Новости'),
        ('events', 'События'),
        ('tips', 'Советы'),
        ('recipes', 'Рецепты'),
    ]

    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField('Краткое описание', blank=True, help_text='Краткое описание для карточки')
    text = models.TextField('Текст')
    image = models.ImageField('Изображение', upload_to='blog/', blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='blog_posts',
        null=True,
        blank=True,
    )
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='news')
    tags = models.CharField('Теги', max_length=200, blank=True, help_text='Через запятую')
    is_published = models.BooleanField('Опубликовано', default=True)
    is_featured = models.BooleanField('Рекомендуемый', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    @property
    def read_time(self):
        words = len(self.text.split())
        return max(1, words // 200)

    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='blog_comments', null=True, blank=True)
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} -> {self.post}'
