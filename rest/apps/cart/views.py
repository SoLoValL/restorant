from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CheckoutSerializer
from apps.promotions.models import PromoCode
from django.utils import timezone


class CartViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """Корзина пользователя"""

    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
            defaults={'session_key': self.request.session.session_key}
            if self.request.user.is_authenticated else {}
        )
        return cart

    def get_queryset(self):
        return Cart.objects.filter(
            user=self.request.user
        ) if self.request.user.is_authenticated else Cart.objects.none()

    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Оформление заказа из корзины"""
        cart = self.get_object()
        if cart.total_items == 0:
            return Response(
                {'error': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка промокода
        promo_code = request.data.get('promo_code')
        discount = 0
        if promo_code:
            try:
                pc = PromoCode.objects.get(
                    code=promo_code,
                    is_active=True,
                    valid_from__lte=timezone.now(),
                    valid_until__gte=timezone.now(),
                )
                if cart.total_price < pc.min_order_amount:
                    return Response(
                        {'error': f'Минимальная сумма заказа: {pc.min_order_amount}'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if pc.discount_type == 'percent':
                    discount = cart.total_price * pc.discount_value / 100
                else:
                    discount = pc.discount_value
                pc.used_count += 1
                pc.save(update_fields=['used_count'])
            except PromoCode.DoesNotExist:
                return Response(
                    {'error': 'Промокод не найден или истёк'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Списание баллов лояльности
        points_to_use = request.data.get('use_points')
        loyalty_discount = 0
        if points_to_use and request.user.is_authenticated:
            try:
                loyalty_card = request.user.loyalty_card
                points_available = min(int(points_to_use), loyalty_card.points_balance)
                loyalty_discount = points_available  # 1 балл = 1 рубль
            except:
                pass

        total_discount = discount + loyalty_discount
        final_total = max(0, cart.total_price - total_discount)

        serializer = CheckoutSerializer({
            'items': CartItemSerializer(cart.items.all(), many=True).data,
            'subtotal': str(cart.total_price),
            'discount': str(total_discount),
            'final_total': str(final_total),
            'promo_code': promo_code,
        })

        # Здесь можно создать реальный заказ — вызов из orders
        # order = OrderService.create_from_cart(cart, user=request.user)
        # cart.items.all().delete()

        return Response(serializer.data)


class CartItemViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Элементы корзины"""

    serializer_class = CartItemSerializer

    def get_cart(self):
        try:
            session_key = self.request.session.session_key
        except:
            session_key = ''
        cart, _ = Cart.objects.get_or_create(
            user=self.request.user if self.request.user.is_authenticated else None,
            defaults={'session_key': session_key}
        )
        return cart

    def get_queryset(self):
        return CartItem.objects.filter(cart=self.get_cart())

    def perform_create(self, serializer):
        cart = self.get_cart()
        serializer.save(cart=cart)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cart_id = instance.cart_id
        self.perform_destroy(instance)
        # Обновляем корзину
        cart = Cart.objects.filter(id=cart_id).first()
        if cart:
            data = CartSerializer(cart).data
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
