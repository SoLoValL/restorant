from django.db import models


class Allergen(models.Model):
    """Аллерген (глютен, лактоза, орехи и т.д.)"""

    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
    severity = models.CharField(
        'Степень опасности',
        max_length=20,
        choices=[('low', 'Низкая'), ('medium', 'Средняя'), ('high', 'Высокая')],
        default='medium',
    )
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Аллерген'
        verbose_name_plural = 'Аллергены'

    def __str__(self):
        return self.name


class Category(models.Model):
    ICON_CHOICES = [
        ('salad', 'Салаты'),
        ('soup', 'Супы'),
        ('meat', 'Мясо'),
        ('fish', 'Рыба'),
        ('pizza', 'Пицца'),
        ('dessert', 'Десерты'),
        ('drink', 'Напитки'),
        ('snack', 'Закуски'),
        ('other', 'Другое'),
    ]

    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField('Иконка', max_length=20, choices=ICON_CHOICES, default='other')
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Фото категории', upload_to='categories/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    @property
    def dishes_count(self):
        return self.dishes.filter(is_available=True).count()


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField()
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    weight = models.CharField('Вес/объём', max_length=50, blank=True)
    image = models.ImageField(upload_to='dishes/', blank=True)
    is_vegetarian = models.BooleanField('Вегетарианское', default=False)
    is_available = models.BooleanField('В наличии', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_hit = models.BooleanField('Хит', default=False)
    allergens = models.ManyToManyField('menu.Allergen', blank=True, related_name='dishes')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('category', 'slug')
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name
