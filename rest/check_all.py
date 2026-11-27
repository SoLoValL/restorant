import urllib.request
import json
import sys

BASE = 'http://127.0.0.1:8000'

endpoints = [
    ('GET', 'categories/', 'Список категорий'),
    ('GET', 'dishes/', 'Список блюд'),
    ('GET', 'dishes/?page_size=1', 'API блюд (1 шт)'),
    ('GET', 'allergens/', 'Список аллергенов'),
    ('GET', 'tables/', 'Список столиков'),
    ('GET', 'reservations/', 'Бронирования'),
    ('GET', 'posts/', 'Посты блога'),
    ('GET', 'comments/', 'Комментарии'),
    ('GET', 'events/', 'События'),
    ('GET', 'event-bookings/', 'Бронирования событий'),
    ('GET', 'orders/', 'Заказы'),
    ('GET', 'order-items/', 'Товары заказов'),
    ('GET', 'reviews/', 'Отзывы'),
    ('GET', 'dish-reviews/', 'Отзывы к блюдам'),
    ('GET', 'promos/', 'Промокоды'),
    ('GET', 'combos/', 'Комбо'),
    ('GET', 'cart/', 'Корзина'),
    ('GET', 'cart-items/', 'Товары корзины'),
    ('GET', 'analytics/overview/', 'Аналитика (overview)'),
    ('GET', 'analytics/popular-dishes/', 'Популярные блюда'),
    ('GET', 'analytics/dish-ratings/', 'Рейтинги блюд'),
    ('GET', 'analytics/top-customers/', 'Топ клиентов'),
    ('GET', 'analytics/reservations-stats/', 'Статистика бронирований'),
]

passed = 0
failed = 0
errors = []

for method, path, desc in endpoints:
    try:
        url = BASE + '/' + path
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req, timeout=10)
        data = r.read().decode()
        try:
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                count = json_data.get('count', 'N/A')
                results = json_data.get('results', [])
                if isinstance(results, list):
                    info = f'{len(results)} items'
                else:
                    info = 'data'
            elif isinstance(json_data, list):
                info = f'{len(json_data)} items'
            else:
                info = 'data'
            status = f'{r.status} ({info})'
        except:
            status = f'{r.status} ({len(data)} bytes)'
        print(f'  PASS  {status:30s} {desc}')
        passed += 1
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode()[:200]
        except:
            pass
        print(f'  FAIL  HTTP {e.code:3d}    {desc}')
        print(f'         {body}')
        failed += 1
        errors.append((path, str(e)))
    except Exception as e:
        print(f'  FAIL  {str(e)[:60]:60s} {desc}')
        failed += 1
        errors.append((path, str(e)))

print(f'\n{"="*70}')
print(f'Итого: {passed} OK, {failed} FAIL из {len(endpoints)}')
if errors:
    print(f'\nОшибки:')
    for path, err in errors:
        print(f'  - {path}: {err[:80]}')
else:
    print('Все API работают!')

sys.exit(0 if failed == 0 else 1)
