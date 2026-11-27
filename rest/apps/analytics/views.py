from django.db.models import Sum, Count, Avg, Q, F
from django.db import models
from django.utils import timezone
from datetime import timedelta
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings

from apps.orders.models import Order, OrderItem
from apps.menu.models import Dish
from apps.reservations.models import Reservation
from apps.reviews.models import Review, DishReview


class AnalyticsViewSet(viewsets.GenericViewSet):
    """Аналитика и статистика"""

    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        """Список доступных аналитических эндпоинтов"""
        return Response({
            'overview': '/analytics/overview/',
            'popular_dishes': '/analytics/popular-dishes/',
            'daily_revenue': '/analytics/daily-revenue/',
            'dish_ratings': '/analytics/dish-ratings/',
            'top_customers': '/analytics/top-customers/',
            'reservations_stats': '/analytics/reservations-stats/',
        })

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Общая статистика"""
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        orders_by_status = dict(
            Order.objects.values('status').annotate(
                count=Count('id')
            ).values_list('status', 'count')
        )

        total_reservations = Reservation.objects.count()
        active_reservations = Reservation.objects.filter(
            status__in=['pending', 'confirmed']
        ).count()

        total_users = getattr(settings, 'AUTH_USER_MODEL', 'auth.User').objects.count()

        avg_order_value = 0
        if total_orders > 0:
            avg_order_value = total_revenue / total_orders

        return Response({
            'orders': {
                'total': total_orders,
                'revenue': float(total_revenue),
                'average_value': float(avg_order_value),
                'by_status': orders_by_status,
            },
            'reservations': {
                'total': total_reservations,
                'active': active_reservations,
            },
            'users': {
                'total': total_users,
            },
        })

    @action(detail=False, methods=['get'])
    def popular_dishes(self, request):
        """Популярные блюда по заказам"""
        days = int(request.query_params.get('days', 30))
        since = timezone.now() - timedelta(days=days)

        popular = (
            OrderItem.objects.filter(
                order__created_at__gte=since,
                order__status__in=['confirmed']
            )
            .values('dish__name', 'dish__slug')
            .annotate(
                quantity=Sum('quantity'),
                revenue=Sum(F('quantity') * F('price')),
            )
            .order_by('-quantity')[:10]
        )

        return Response({
            'period_days': days,
            'dishes': popular,
        })

    @action(detail=False, methods=['get'])
    def daily_revenue(self, request):
        """Доход по дням"""
        days = int(request.query_params.get('days', 30))
        since = timezone.now() - timedelta(days=days)

        revenue_by_day = (
            Order.objects.filter(
                created_at__gte=since,
                status__in=['confirmed']
            )
            .dates('created_at', 'day')
            .annotate(
                day=models.DateField(),
                revenue=Sum('total_price'),
            )
        )

        return Response({
            'period_days': days,
            'data': [
                {'date': d.strftime('%Y-%m-%d'), 'revenue': float(d.revenue or 0)}
                for d in revenue_by_day
            ],
        })

    @action(detail=False, methods=['get'])
    def dish_ratings(self, request):
        """Рейтинги блюд"""
        dishes = Dish.objects.annotate(
            avg_rating=Avg('dish_reviews__rating'),
            review_count=Count('dish_reviews')
        ).filter(review_count__gt=0).order_by('-avg_rating')[:10]

        data = []
        for dish in dishes:
            data.append({
                'id': dish.id,
                'name': dish.name,
                'avg_rating': round(float(dish.avg_rating or 0), 2),
                'review_count': dish.review_count,
            })

        return Response({'dishes': data})

    @action(detail=False, methods=['get'])
    def top_customers(self, request):
        """Топ клиентов по сумме заказов"""
        top = (
            Order.objects.values('user__username', 'user__email')
            .annotate(
                total_orders=Count('id'),
                total_spent=Sum('total_price'),
            )
            .order_by('-total_spent')[:10]
        )

        return Response({'customers': top})

    @action(detail=False, methods=['get'])
    def reservations_stats(self, request):
        """Статистика бронирований"""
        by_status = dict(
            Reservation.objects.values('status').annotate(
                count=Count('id')
            ).values_list('status', 'count')
        )

        # По дням недели
        day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        reservations_by_day = dict(
            Reservation.objects.extra(select={'day': 'CAST(strftime(\'%w\', date) AS integer)'})
            .values('day')
            .annotate(count=Count('id'))
            .values_list('day', 'count')
        )

        # Среднее количество гостей
        avg_guests = Reservation.objects.aggregate(
            avg=Avg('guests_count')
        )['avg'] or 0

        return Response({
            'by_status': by_status,
            'by_day_of_week': dict(reservations_by_day),
            'average_guests': round(avg_guests, 1),
        })
