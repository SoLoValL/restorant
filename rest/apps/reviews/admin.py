from django.contrib import admin
from .models import Review, DishReview


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')
    search_fields = ('author__username', 'text')


@admin.register(DishReview)
class DishReviewAdmin(admin.ModelAdmin):
    list_display = ('dish', 'author', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating')
    search_fields = ('dish__name', 'author__username', 'text')
