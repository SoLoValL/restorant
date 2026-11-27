from rest_framework import serializers
from .models import Reservation, Table

class TableSerializer(serializers.ModelSerializer):
    zone_label = serializers.CharField(source='get_zone_display', read_only=True)

    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'zone', 'zone_label', 'svg_x', 'svg_y']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id', 'name', 'phone', 'email', 'table',
            'date', 'time', 'guests_count', 'comment', 'status'
        ]
        read_only_fields = ['status']
