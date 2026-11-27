from rest_framework import serializers
from .models import Cart, CartItem
from apps.menu.serializers import DishSerializer


class CartItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)
    dish_id = serializers.PrimaryKeyRelatedField(
        queryset=DishSerializer.Meta.model.objects.all(),
        source='dish',
        write_only=True,
    )
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    dish_image = serializers.ImageField(source='dish.image', read_only=True)
    unit_price = serializers.DecimalField(
        source='dish.price',
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )
    total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = [
            'id', 'dish', 'dish_id', 'dish_name', 'dish_image',
            'unit_price', 'quantity', 'total',
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']


class CheckoutSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    promo_code = serializers.CharField(required=False, allow_blank=True)
