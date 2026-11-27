from rest_framework import serializers
from .models import Allergen, Category, Dish


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['id', 'name', 'slug', 'description', 'severity', 'is_active']


class DishSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)
    allergen_ids = serializers.PrimaryKeyRelatedField(
        queryset=Allergen.objects.all(),
        source='allergens',
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Dish
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'weight', 'image', 'is_vegetarian', 'is_available',
            'is_new', 'is_hit', 'allergens', 'allergen_ids', 'order',
        ]


class CategorySerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'dishes']
