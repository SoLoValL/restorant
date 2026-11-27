from rest_framework import serializers

from apps.menu.models import Dish
from apps.menu.serializers import DishSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    dish_id = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
        source='dish',
        write_only=True,
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'dish_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'name', 'phone', 'address',
            'status', 'total_price', 'items', 'created_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at']
