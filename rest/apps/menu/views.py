from rest_framework import filters, viewsets
from .models import Allergen, Category, Dish
from .serializers import AllergenSerializer, CategorySerializer, DishSerializer


class AllergenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.filter(is_available=True)
    serializer_class = DishSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'allergens__name']
    ordering_fields = ['price', 'name', 'order']
    ordering = ['order']
