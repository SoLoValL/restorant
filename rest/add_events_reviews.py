# -*- coding: utf-8 -*-
import os, sys, django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest1.settings')
django.setup()

from apps.reviews.models import Review
from django.contrib.auth import get_user_model
User = get_user_model()

users = list(User.objects.all())
print(f"Users: {[u.username for u in users]}")

# Удалим существующие
Review.objects.all().delete()

# Добавим 5 отзывов
reviews = [
    ('Потрясающая атмосфера! Приходим с семьёй каждые выходные. Дети в восторге от десертов.', 5, users[0] if len(users) > 0 else None),
    ('Отличное место для делового ужина. Тихо, быстро обслуживают, паста Карбонара — лучшая в городе.', 5, users[1] if len(users) > 1 else users[0]),
    ('Были на мастер-классе по пасте — незабываемые впечатления! Шеф Марко настоящий профессионал.', 5, users[0] if len(users) > 0 else None),
    ('Вино и сыр — просто волшебство. Сомелье Анна подобрала идеальные пары. Рекомендую!', 4, users[1] if len(users) > 1 else users[0]),
    ('Прекрасный ресторан с уютной атмосферой. Еда того стоит, хотя в пятницу бывает шумновато.', 4, users[0] if len(users) > 0 else None),
]

for text, rating, author in reviews:
    Review.objects.create(text=text, rating=rating, is_published=True, author=author)
    print(f'  Added: {text[:40]}...')

print(f'\nDone! Total reviews: {Review.objects.count()}')
