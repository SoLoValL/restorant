from rest_framework import mixins, viewsets

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer
from apps.notifications.services import NotificationService
from apps.loyalty.views import LoyaltyViewSet


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(user=user)
        return queryset.none()

    def perform_create(self, serializer):
        order = serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None
        )

        # Отправляем уведомление о создании заказа
        if order.user:
            NotificationService.send_order_created(order)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        order = self.get_object()

        # Уведомление при подтверждении заказа
        if order.status == 'confirmed':
            NotificationService.send_order_confirmation(order)

            # Начисление баллов лояльности
            if order.user:
                try:
                    loyalty = LoyaltyViewSet()
                    loyalty.request = request
                    loyalty.perform_point_earn(order)
                    NotificationService.send_points_earned(
                        order.user,
                        int(order.total_price),
                        order,
                    )
                except:
                    pass

        return response


class OrderItemViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
