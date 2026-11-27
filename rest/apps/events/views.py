from rest_framework import mixins, viewsets

from .models import Event, EventBooking
from .serializers import EventBookingSerializer, EventSerializer


class EventViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer


class EventBookingViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = EventBooking.objects.all()
    serializer_class = EventBookingSerializer
