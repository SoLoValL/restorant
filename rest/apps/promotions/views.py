from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response
from django.utils import timezone
from .models import PromoCode, Combo
from .serializers import PromoCodeSerializer, ComboSerializer


class PromoCodeViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    queryset = PromoCode.objects.filter(is_active=True, valid_until__gte=timezone.now())
    serializer_class = PromoCodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code']

    def perform_create(self, serializer):
        # При использовании промокода увеличиваем счётчик
        promo = serializer.save()
        promo.used_count += 1
        promo.save(update_fields=['used_count'])


class ComboViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Combo.objects.filter(is_active=True, is_available=True)
    serializer_class = ComboSerializer
