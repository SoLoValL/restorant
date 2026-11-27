from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

from .models import DishReview, Review
from .serializers import DishReviewSerializer, ReviewSerializer


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.filter(is_published=True)
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else None)


class DishReviewViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = DishReviewSerializer

    def get_queryset(self):
        qs = DishReview.objects.filter(is_published=True)
        dish_slug = self.request.query_params.get('dish')
        if dish_slug:
            qs = qs.filter(dish__slug=dish_slug)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Статистика отзывов по блюду"""
        instance = self.get_object()
        avg_rating = instance.dish_reviews.filter(is_published=True).aggregate(
            avg=Avg('rating')
        )['avg'] or 0
        total = instance.dish_reviews.filter(is_published=True).count()
        return Response({
            'dish': instance.dish.name,
            'average_rating': round(avg_rating, 2),
            'total_reviews': total,
        })
