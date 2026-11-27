from django.contrib import admin
from .models import Category, Dish, Allergen


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity', 'is_active')
    list_filter = ('severity', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_new', 'is_hit')
    list_filter = ('is_available', 'is_vegetarian', 'is_new', 'is_hit', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('allergens',)
