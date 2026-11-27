from django.contrib import admin
from .models import LoyaltyCard, PointsHistory


@admin.register(LoyaltyCard)
class LoyaltyCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points_balance', 'level', 'discount_percent', 'registered_at')
    list_filter = ('level',)
    search_fields = ('user__username', 'user__email')


@admin.register(PointsHistory)
class PointsHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'operation_type', 'order', 'created_at')
    list_filter = ('operation_type',)
    search_fields = ('user__username', 'description')
