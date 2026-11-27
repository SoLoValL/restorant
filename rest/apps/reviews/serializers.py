from rest_framework import serializers
from .models import DishReview, Review


class DishReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    dish_slug = serializers.SlugField(source='dish.slug', read_only=True)

    class Meta:
        model = DishReview
        fields = [
            'id', 'dish', 'dish_name', 'dish_slug', 'author', 'author_name',
            'rating', 'text', 'is_published', 'created_at',
        ]
        read_only_fields = ['id', 'author', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'author_name', 'rating',
                  'text', 'is_published', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return value
