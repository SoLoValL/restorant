from rest_framework import serializers
from .models import LoyaltyCard, PointsHistory


class LoyaltyCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyCard
        fields = [
            'id', 'user', 'points_balance', 'total_earned',
            'total_spent', 'level', 'discount_percent', 'registered_at',
        ]
        read_only_fields = fields


class PointsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsHistory
        fields = [
            'id', 'user', 'points', 'operation_type',
            'description', 'order', 'created_at',
        ]
        read_only_fields = fields
