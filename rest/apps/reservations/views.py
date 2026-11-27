from rest_framework import viewsets, mixins
from .models import Reservation, Table
from .serializers import ReservationSerializer, TableSerializer
from apps.notifications.services import NotificationService


class ReservationViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        reservation = serializer.save()
        # Отправляем email о подтверждении бронирования
        NotificationService.send_reservation_confirmation(reservation)


class TableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.filter(is_active=True)
    serializer_class = TableSerializer
