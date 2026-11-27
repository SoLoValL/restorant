from rest_framework import serializers
from .models import Event, EventBooking


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'image',
            'date', 'time', 'price', 'is_active'
        ]
        read_only_fields = ['id', 'slug']


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = [
            'id', 'event', 'name', 'phone', 'email',
            'guests_count', 'comment', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
