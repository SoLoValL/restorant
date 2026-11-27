from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.analytics.views import AnalyticsViewSet
from apps.cart.views import CartViewSet, CartItemViewSet
from apps.core.views import home, restaurant_map, check_table_availability
from apps.blog.views import CommentViewSet, PostViewSet
from apps.events.views import EventBookingViewSet, EventViewSet
from apps.loyalty.views import LoyaltyViewSet, PointsHistoryViewSet
from apps.menu.views import AllergenViewSet, CategoryViewSet, DishViewSet
from apps.orders.views import OrderItemViewSet, OrderViewSet
from apps.promotions.views import PromoCodeViewSet, ComboViewSet
from apps.reservations.views import ReservationViewSet, TableViewSet
from apps.reviews.views import ReviewViewSet, DishReviewViewSet
from apps.users.views import RegisterView

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('dishes', DishViewSet)
router.register('allergens', AllergenViewSet, basename='allergen')
router.register('tables', TableViewSet)
router.register('reservations', ReservationViewSet, basename='reservation')
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')
router.register('events', EventViewSet, basename='event')
router.register('event-bookings', EventBookingViewSet, basename='event-booking')
router.register('orders', OrderViewSet, basename='order')
router.register('order-items', OrderItemViewSet, basename='order-item')
router.register('reviews', ReviewViewSet, basename='review')
router.register('dish-reviews', DishReviewViewSet, basename='dish-review')
router.register('promos', PromoCodeViewSet, basename='promo')
router.register('combos', ComboViewSet, basename='combo')
router.register('loyalty', LoyaltyViewSet, basename='loyalty')
router.register('points-history', PointsHistoryViewSet, basename='points-history')
router.register('cart', CartViewSet, basename='cart')
router.register('cart-items', CartItemViewSet, basename='cart-item')
router.register('analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('map/', restaurant_map, name='restaurant_map'),
    path('check-table-availability/', check_table_availability, name='check_table_availability'),
] + router.urls

# Раздача media-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    for static_dir in settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=str(static_dir))

