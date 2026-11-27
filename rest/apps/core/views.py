from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from apps.menu.models import Category, Dish
from apps.blog.models import Post
from apps.events.models import Event
from apps.reviews.models import Review
from apps.reservations.models import Table, Reservation
from apps.reservations.serializers import TableSerializer


def home(request):
    context = {
        'categories': Category.objects.prefetch_related('dishes').filter(is_active=True).all(),
        'dishes': Dish.objects.filter(is_available=True)[:6],
        'posts': Post.objects.filter(is_published=True)[:3],
        'events': Event.objects.filter(is_active=True, is_featured=True)[:3] or Event.objects.filter(is_active=True)[:3],
        'reviews': Review.objects.filter(is_published=True)[:3],
    }
    return render(request, 'home.html', context)


def restaurant_map(request):
    """Restaurant map view with table selection."""
    tables = Table.objects.filter(is_active=True).order_by('zone', 'number')
    tables_data = TableSerializer(tables, many=True).data
    return render(request, 'restaurant_map.html', {
        'tables': tables_data,
        'zone_choices': Table._meta.get_field('zone').choices,
    })


def check_table_availability(request):
    """API endpoint to check if a table is available for a given date and time."""
    if request.method != 'GET':
        return JsonResponse({'error': 'GET only'}, status=405)

    table_id = request.GET.get('table_id')
    date = request.GET.get('date')
    time = request.GET.get('time')

    if not all([table_id, date, time]):
        return JsonResponse({'error': 'table_id, date, and time are required'}, status=400)

    try:
        table = Table.objects.get(id=table_id)
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Table not found'}, status=404)

    # Check for overlapping reservations (same date and within 3 hours of the requested time)
    from datetime import datetime
    try:
        req_date = datetime.strptime(date, '%Y-%m-%d').date()
        req_time = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        return JsonResponse({'error': 'Invalid date or time format'}, status=400)

    # Reservations on the same date within 3-hour window
    overlapping = Reservation.objects.filter(
        table=table,
        date=req_date,
        status__in=['pending', 'confirmed'],
    ).exclude(status='cancelled')

    is_available = True
    conflicts = []
    for res in overlapping:
        res_start = res.time
        res_end_minutes = res_start.hour * 60 + res_start.minute + 180  # 3-hour reservation
        req_start_minutes = req_time.hour * 60 + req_time.minute
        req_end_minutes = req_start_minutes + 180

        if not (req_end_minutes <= res_start.hour * 60 + res_start.minute or
                req_start_minutes >= res_end_minutes):
            is_available = False
            conflicts.append({
                'id': res.id,
                'time': res.time.strftime('%H:%M'),
                'name': res.name,
            })

    return JsonResponse({
        'available': is_available,
        'table': {
            'id': table.id,
            'number': table.number,
            'capacity': table.capacity,
            'zone_label': table.get_zone_display(),
        },
        'conflicts': conflicts,
    })
