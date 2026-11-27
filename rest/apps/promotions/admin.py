from django.contrib import admin
from .models import PromoCode, Combo


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'is_active', 'used_count', 'valid_from', 'valid_until')
    list_filter = ('is_active', 'discount_type')
    search_fields = ('code', 'description')


@admin.register(Combo)
class ComboAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'original_price', 'is_active', 'is_available')
    list_filter = ('is_active', 'is_available')
    search_fields = ('name', 'description')
    filter_horizontal = ('dishes',)
