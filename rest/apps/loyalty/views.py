from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LoyaltyCard, PointsHistory
from .serializers import LoyaltyCardSerializer, PointsHistorySerializer


class LoyaltyViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Просмотр карты лояльности и начисление баллов за заказ"""

    serializer_class = LoyaltyCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoyaltyCard.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            # Создаём карту лояльности при первом обращении
            LoyaltyCard.objects.create(user=request.user)
            queryset = self.get_queryset()
        instance = queryset.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_point_earn(self, order):
        """Начислить баллы за заказ (вызывать из views заказов)"""
        card, created = LoyaltyCard.objects.get_or_create(user=order.user)
        points = int(order.total_price)  # 1 балл за 1 рубль
        card.points_balance += points
        card.total_earned += points
        card.calculate_level()
        card.save()

        PointsHistory.objects.create(
            user=order.user,
            points=points,
            operation_type='earned',
            description=f'Начислено за заказ #{order.pk}',
            order=order,
        )


class PointsHistoryViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """История операций с баллами"""

    serializer_class = PointsHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PointsHistory.objects.filter(user=self.request.user)
