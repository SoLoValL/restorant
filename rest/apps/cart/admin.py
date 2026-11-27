from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'total_items', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'session_key')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'dish', 'quantity', 'total')
    list_filter = ('cart__user',)
    search_fields = ('dish__name',)
