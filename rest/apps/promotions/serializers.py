from rest_framework import serializers
from .models import PromoCode, Combo
from apps.menu.serializers import DishSerializer, CategorySerializer
from apps.menu.models import Dish


class PromoCodeSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    remaining_uses = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = PromoCode
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'min_order_amount', 'is_active', 'is_valid', 'usage_limit',
            'used_count', 'remaining_uses', 'valid_from', 'valid_until',
            'applicable_categories', 'created_at',
        ]


class ComboSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    dish_ids = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
        source='dishes',
        many=True,
        write_only=True,
        required=False,
    )
    savings = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True, required=False)
    savings_percent = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True, required=False)

    class Meta:
        model = Combo
        fields = [
            'id', 'name', 'slug', 'description', 'image', 'price',
            'original_price', 'is_active', 'is_available', 'dishes',
            'dish_ids', 'savings', 'savings_percent', 'order',
        ]
