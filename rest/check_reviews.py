# -*- coding: utf-8 -*-
import os, sys, django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest1.settings')
django.setup()

from apps.reviews.models import Review
from django.contrib.auth import get_user_model
User = get_user_model()

users = list(User.objects.all())
print(f"Users available: {len(users)}")
for u in users:
    print(f"  - {u.username} ({u.email})")

# Посмотрим текущие отзывы
existing = Review.objects.filter(is_published=True)
print(f"\nExisting published reviews: {existing.count()}")
for r in existing:
    print(f"  - {r.author.username}: {r.text[:50]}...")
