# -*- coding: utf-8 -*-
"""
Seed script for test data.
Usage: python seed.py
"""
import os
import sys
import django
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest1.settings')
django.setup()

from apps.menu.models import Category, Dish, Allergen
from apps.blog.models import Post
from apps.promotions.models import PromoCode, Combo
from apps.reservations.models import Table
from apps.reviews.models import Review, DishReview
from apps.orders.models import Order, OrderItem
from datetime import date, time, timedelta
from decimal import Decimal
from django.utils import timezone

User = get_user_model()
BASE_DIR = Path(__file__).resolve().parent
MEDIA_BASE = BASE_DIR / 'media'


def seed_data():
    print("Seeding database...")

    # Create admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@restaurant.ru', 'admin123')
        print("  Admin created: admin / admin123")

    # Create test user
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user('testuser', 'test@test.ru', 'test123')
        user.first_name = 'Test'
        user.last_name = 'User'
        user.phone = '+79991234567'
        user.save()
        print("  Test user created: testuser / test123")

    # Allergens
    allergens_data = [
        ('Глютен', 'gluten', 'Пшеница, рожь, ячень', 'high'),
        ('Лактоза', 'lactose', 'Молочные продукты', 'medium'),
        ('Орехи', 'nuts', 'Миндаль, грецкий, кешью', 'high'),
        ('Яйца', 'eggs', 'Куриные яйца', 'high'),
        ('Соя', 'soy', 'Соевые продукты', 'medium'),
        ('Морепродукты', 'seafood', 'Рыба, креветки, крабы', 'high'),
        ('Горчица', 'mustard', 'Горчичные семена', 'medium'),
        ('Сельдерей', 'celery', 'Стебли сельдерея', 'low'),
    ]

    allergens = {}
    for name, slug, desc, severity in allergens_data:
        allergen, created = Allergen.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'description': desc, 'severity': severity}
        )
        allergens[slug] = allergen
        if created:
            print(f"  Allergen: {name}")

    # Categories с описанием и иконками
    categories_data = [
        ('Закуски', 'starters', 'snack', 'Лёгкие блюда для начала ужина', 1, 'starters.jpg'),
        ('Салаты', 'salads', 'salad', 'Свежие овощи и зелень', 2, 'salads.jpg'),
        ('Супы', 'soups', 'soup', 'Ароматные супы на каждый день', 3, 'soups.jpg'),
        ('Горячие блюда', 'main-course', 'meat', 'Основные блюда из мяса и птицы', 4, 'main-course.jpg'),
        ('Пицца', 'pizza', 'pizza', 'Итальянская классика', 5, 'pizza.jpg'),
        ('Десерты', 'desserts', 'dessert', 'Сладкий финал ужина', 6, 'desserts.jpg'),
        ('Напитки', 'drinks', 'drink', 'Горячие и холодные напитки', 7, 'drinks.jpg'),
    ]

    categories = {}
    for name, slug, icon, desc, order, img_name in categories_data:
        category, created = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'icon': icon, 'description': desc, 'order': order}
        )
        categories[slug] = category
        if created:
            print(f"  Category: {name}")
        
        # Загрузка изображения категории (локальный файл)
        if img_name:
            try:
                local_path = MEDIA_BASE.parent / 'categories' / img_name
                if local_path.exists() and not category.image:
                    with open(local_path, 'rb') as f:
                        img_data = f.read()
                    category.image.save(img_name, ContentFile(img_data), save=True)
                    print(f"  Category image OK: {name}")
            except Exception as e:
                print(f"  Category image FAIL: {name}: {str(e)[:50]}")

    # Dishes с фото (локальные файлы)
    dishes_data = [
        ('Брускетта с томатами', 'starters', 'Тосты с томатами, базиликом', Decimal('390'), '200 г', False, False, ['gluten'],
         'bruschetta-tomatoes.jpg'),
        ('Канапе с лососем', 'starters', 'Батончики с лососем и сыром', Decimal('520'), '150 г', False, False, ['eggs', 'seafood'],
         'canapes-salmon.jpg'),
        ('Оливье', 'starters', 'Классический оливье', Decimal('350'), '250 г', False, False, ['eggs', 'lactose'],
         'olivier.jpg'),
        ('Цезарь с курицей', 'salads', 'Романо, курица, пармезан', Decimal('480'), '300 г', False, True, ['lactose', 'eggs'],
         'caesar-chicken.jpg'),
        ('Греческий', 'salads', 'Томаты, огурцы, оливки, фета', Decimal('420'), '350 г', True, True, ['lactose'],
         'greek-salad.jpg'),
        ('Витаминный', 'salads', 'Капуста, морковь, яблоко', Decimal('280'), '250 г', True, True, [],
         'vitamin-salad.jpg'),
        ('Том Ям', 'soups', 'Тайский суп с креветками', Decimal('550'), '400 мл', False, True, ['seafood'],
         'tom-yam.jpg'),
        ('Крем-суп грибной', 'soups', 'Шампиньоны, сливки', Decimal('420'), '350 мл', False, True, ['gluten', 'lactose'],
         'mushroom-soup.jpg'),
        ('Борщ', 'soups', 'Классический борщ', Decimal('380'), '400 мл', False, True, ['lactose'],
         'borscht.jpg'),
        ('Стейк рибай', 'main-course', 'Говядина, 300г, овощи гриль', Decimal('1890'), '450 г', False, True, [],
         'ribeye-steak.jpg'),
        ('Паста Карбонара', 'main-course', 'Спагетти, бекон, пармезан', Decimal('580'), '350 г', False, True, ['gluten', 'eggs', 'lactose'],
         'pasta-carbonara.jpg'),
        ('Курица Тикка Масала', 'main-course', 'Курица в остром соусе', Decimal('620'), '400 г', False, True, ['lactose'],
         'chicken-tikka.jpg'),
        ('Веган-боул', 'main-course', 'Киноа, авокадо, нут', Decimal('520'), '350 г', True, True, [],
         'vegan-bowl.jpg'),
        ('Маргарита', 'pizza', 'Томатный соус, моцарелла', Decimal('590'), '400 г', False, True, ['gluten', 'lactose'],
         'pizza-margarita.jpg'),
        ('Пепперони', 'pizza', 'Пепперони, моцарелла', Decimal('690'), '450 г', False, True, ['gluten', 'lactose'],
         'pizza-pepperoni.jpg'),
        ('Четыре сыра', 'pizza', 'Моцарелла, горгонзола', Decimal('790'), '400 г', False, True, ['gluten', 'lactose'],
         'pizza-four-cheeses.jpg'),
        ('Тирамису', 'desserts', 'Маскарпоне, савоярди', Decimal('450'), '200 г', False, True, ['gluten', 'eggs', 'lactose'],
         'tiramisu.jpg'),
        ('Чизкейк', 'desserts', 'Сливочный сыр', Decimal('480'), '200 г', False, True, ['gluten', 'eggs', 'lactose'],
         'cheesecake.jpg'),
        ('Лимонад домашний', 'drinks', 'Лимон, мята', Decimal('250'), '500 мл', True, True, [],
         'lemonade.jpg'),
        ('Капучино', 'drinks', 'Эспрессо, молоко', Decimal('280'), '300 мл', False, True, ['lactose'],
         'cappuccino.jpg'),
    ]

    for name, cat_slug, desc, price, weight, veg, available, allergen_slugs, image_url in dishes_data:
        dish, created = Dish.objects.get_or_create(
            slug=name.lower().replace(' ', '-'),
            defaults={
                'name': name,
                'category': categories[cat_slug],
                'description': desc,
                'price': price,
                'weight': weight,
                'is_vegetarian': veg,
                'is_available': available,
            }
        )
        dish.allergens.set([allergens[slug] for slug in allergen_slugs if slug in allergens])
        if created:
            print(f"  Dish: {name}")

    # Загрузка изображений (локальные файлы)
    print("\nLoading images...")
    MEDIA_BASE = BASE_DIR / 'media' / 'dishes'
    for dish in Dish.objects.all():
        if not dish.image:
            try:
                # Ищем dish в dishes_data по имени
                for _, _, _, _, _, _, _, _, image_name in dishes_data:
                    if not image_name:
                        continue
                    local_path = MEDIA_BASE / image_name
                    if local_path.exists():
                        with open(local_path, 'rb') as f:
                            img_data = f.read()
                        dish.image.save(image_name, ContentFile(img_data), save=True)
                        print(f"  OK {dish.name}")
                        break
            except Exception as e:
                print(f"  FAIL {dish.name}: {str(e)[:50]}")

    # Combos
    combos_data = [
        ('Комбо на двоих', 'combo-for-two', 'Паста + Борщ + Тирамису', Decimal('1490'), Decimal('1950'), ['main-course', 'soups', 'desserts']),
        ('Обед бизнес', 'business-lunch', 'Суп + Горячее + Напиток', Decimal('690'), Decimal('950'), ['soups', 'main-course', 'drinks']),
    ]

    for name, slug, desc, price, orig_price, cat_slugs in combos_data:
        combo, created = Combo.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': desc,
                'price': price,
                'original_price': orig_price,
            }
        )
        for cat_slug in cat_slugs:
            combo.dishes.add(*categories[cat_slug].dishes.all()[:2])
        if created:
            print(f"  Combo: {name}")

    # Promo codes
    now = timezone.now()
    promos_data = [
        ('WELCOME10', 'Скидка 10%', 'percent', Decimal('10'), Decimal('1000'), 50, 10, -30),
        ('BIG20', 'Скидка 20%', 'percent', Decimal('20'), Decimal('2000'), 100, 10, -30),
    ]

    for code, desc, dtype, discount, min_amount, limit, days_from, days_until in promos_data:
        PromoCode.objects.get_or_create(
            code=code,
            defaults={
                'description': desc,
                'discount_type': dtype,
                'discount_value': discount,
                'min_order_amount': min_amount,
                'usage_limit': limit,
                'valid_from': now + timedelta(days=days_from),
                'valid_until': now + timedelta(days=days_until),
            }
        )
        print(f"  Promo: {code}")

    # Tables with zones and map coordinates
    tables_data = [
        # Main Hall (x: 100-300, y: 80-200)
        (1, 2, 'main_hall', 120, 100),
        (2, 2, 'main_hall', 200, 100),
        (3, 4, 'main_hall', 280, 100),
        (4, 4, 'main_hall', 120, 160),
        (5, 6, 'main_hall', 200, 160),
        # Terrace (x: 450-650, y: 50-120)
        (6, 2, 'terrace', 450, 70),
        (7, 8, 'terrace', 580, 70),
        (8, 2, 'terrace', 700, 70),
        # VIP (x: 60-160, y: 320-420)
        (9, 4, 'vip', 80, 350),
        (10, 6, 'vip', 160, 350),
        # Window (x: 280-380, y: 320-420)
        (11, 2, 'window', 280, 350),
        (12, 4, 'window', 360, 350),
        # Bar (x: 500-700, y: 250-400)
        (13, 2, 'bar', 500, 280),
        (14, 2, 'bar', 600, 280),
        (15, 4, 'bar', 700, 280),
        (16, 2, 'bar', 500, 360),
        (17, 2, 'bar', 600, 360),
        (18, 4, 'bar', 700, 360),
    ]

    for number, capacity, zone, svg_x, svg_y in tables_data:
        Table.objects.get_or_create(
            number=number,
            defaults={'capacity': capacity, 'is_active': True, 'zone': zone, 'svg_x': svg_x, 'svg_y': svg_y}
        )
        print(f"  Table: #{number} ({capacity} seats) — {zone} ({svg_x},{svg_y})")

    # Reviews
    if User.objects.filter(username='testuser').exists():
        testuser = User.objects.get(username='testuser')
        dishes = list(Dish.objects.filter(is_available=True)[:5])

        for i, (text, rating) in enumerate([
            ('Потрясающий стейк!', 5),
            ('Паста была отличной', 4),
            ('Борщ как у бабушки', 5),
        ]):
            if dishes:
                dish = dishes[i % len(dishes)]
                Review.objects.get_or_create(
                    author=testuser,
                    defaults={'rating': rating, 'text': text, 'is_published': True}
                )
                DishReview.objects.get_or_create(
                    dish=dish, author=testuser,
                    defaults={'rating': rating, 'text': text, 'is_published': True}
                )
                print(f"  Review: {text}")

    # Blog posts
    posts_data = [
        ('Искусство приготовления стейков', 'cooking-steaks', 'Кухня',
         'Рассказываем, как правильно выбрать и приготовить стейк средней прожарки. Секреты шеф-повара.',
         'steaks.jpg', True, 'стейк,мясо,гриль', True),
        ('Новое меню на осень', 'autumn-menu', 'Новости',
         'Представляем сезонное меню с тыквами, грибами и пряными специями. 15 новых блюд!',
         'autumn-menu.jpg', True, 'сезонное,новинки', False),
        ('Вино и еда: идеальные сочетания', 'wine-pairing', 'Советы',
         'Как правильно сочетать вина с блюдами. Гид от нашего сомелье по парам.',
         'wine-pairing.jpg', True, 'вино,гастрономия', True),
    ]

    for title, slug, cat, excerpt, img_name, published, tags, featured in posts_data:
        post, created = Post.objects.get_or_create(
            slug=slug,
            defaults={
                'title': title,
                'category': cat,
                'excerpt': excerpt,
                'text': f'{excerpt} {excerpt} {excerpt} {excerpt}',
                'is_published': published,
                'tags': tags,
                'is_featured': featured,
                'author': testuser,
            }
        )
        if created:
            print(f"  Post: {title}")
        
        # Загрузка изображения поста (локальный файл)
        if img_name and not post.image:
            try:
                local_path = MEDIA_BASE.parent / 'blog' / img_name
                if local_path.exists():
                    with open(local_path, 'rb') as f:
                        img_data = f.read()
                    post.image.save(img_name, ContentFile(img_data), save=True)
                    print(f"  Post image OK: {title}")
            except Exception as e:
                print(f"  Post image FAIL: {title}: {str(e)[:50]}")

    print("\nDone!")
    print(f"  Users: {User.objects.count()}")
    print(f"  Allergens: {Allergen.objects.count()}")
    print(f"  Categories: {Category.objects.count()}")
    print(f"  Dishes: {Dish.objects.count()}")
    print(f"  Combos: {Combo.objects.count()}")
    print(f"  Promos: {PromoCode.objects.count()}")
    print(f"  Tables: {Table.objects.count()}")
    print(f"  Reviews: {Review.objects.count()}")
    print(f"  DishReviews: {DishReview.objects.count()}")
    print(f"  Posts: {Post.objects.count()}")


if __name__ == '__main__':
    seed_data()
