from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


class NotificationService:
    """Сервис отправки уведомлений"""

    @staticmethod
    def create_notification(user, notification_type, title, message):
        """Создать уведомление для пользователя"""
        return Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
        )

    @staticmethod
    def send_order_confirmation(order):
        """Отправить email о подтверждении заказа"""
        subject = f'Заказ #{order.pk} подтверждён'
        message = (
            f'Здравствуйте, {order.name}!\n\n'
            f'Ваш заказ #{order.pk} подтверждён.\n'
            f'Сумма: {order.total_price} руб.\n\n'
            f'Список блюд:\n'
        )
        for item in order.items.all():
            message += f'  - {item.dish.name} x {item.quantity} = {item.dish.price * item.quantity} руб.\n'

        recipient_list = [
            order.user.email
            if order.user and order.user.email
            else None
        ]
        recipient_list = [r for r in recipient_list if r]

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )

        if order.user:
            NotificationService.create_notification(
                user=order.user,
                notification_type='order_confirmed',
                title='Заказ подтверждён',
                message=f'Ваш заказ #{order.pk} на сумму {order.total_price} руб. подтверждён.',
            )

    @staticmethod
    def send_reservation_confirmation(reservation):
        """Отправить email о подтверждении бронирования"""
        subject = f'Бронирование столика подтверждено'
        message = (
            f'Здравствуйте, {reservation.name}!\n\n'
            f'Ваше бронирование подтверждено.\n'
            f'Дата: {reservation.date}\n'
            f'Время: {reservation.time}\n'
            f'Количество гостей: {reservation.guests_count}\n'
        )
        if reservation.table:
            message += f'Столик №{reservation.table.number}\n'
        if reservation.comment:
            message += f'Комментарий: {reservation.comment}\n'

        recipient_list = [
            reservation.email
            if reservation.email
            else None
        ]
        recipient_list = [r for r in recipient_list if r]

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )

    @staticmethod
    def send_order_created(order):
        """Отправить email о создании заказа"""
        subject = f'Заказ #{order.pk} принят в обработку'
        message = (
            f'Здравствуйте, {order.name}!\n\n'
            f'Ваш заказ #{order.pk} принят в обработку.\n'
            f'Сумма: {order.total_price} руб.\n'
            f'Адрес доставки: {order.address}\n\n'
            f'Мы свяжемся с вами для подтверждения.'
        )

        recipient_list = [
            order.user.email
            if order.user and order.user.email
            else None
        ]
        recipient_list = [r for r in recipient_list if r]

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )

        if order.user:
            NotificationService.create_notification(
                user=order.user,
                notification_type='order_created',
                title='Заказ создан',
                message=f'Ваш заказ #{order.pk} на сумму {order.total_price} руб. принят в обработку.',
            )

    @staticmethod
    def send_points_earned(user, points, order):
        """Отправить email о начислении баллов"""
        subject = 'Баллы начислены'
        message = (
            f'Вам начислено {points} бонусных баллов за заказ #{order.pk}.\n'
            f'Ваш баланс: {user.loyalty_card.points_balance} баллов.'
        )

        if user.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

        NotificationService.create_notification(
            user=user,
            notification_type='points_earned',
            title='Баллы начислены',
            message=f'Начислено {points} баллов за заказ #{order.pk}.',
        )
