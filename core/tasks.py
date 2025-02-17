from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(user_email):
    """Фоновая задача для отправки email после оформления заказа"""

    if not user_email or not user_email.strip():
        return "❌ Ошибка: Email не указан!"

    send_mail(
        subject="Подтверждение заказа",
        message="Ваш заказ успешно оформлен! Спасибо за покупку.",
        from_email="priluckijkirill30@gmail.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f'✅ Email отправлен на {user_email}'