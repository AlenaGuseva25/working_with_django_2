from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Subscription, Course
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_inactive_users():
    """Проверка неактивных пользователей"""
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lte=month_ago,
        is_active=True
    ).only('id', 'is_active')

    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.info(f'Пользователь {user.email} заблокирован в связи с неактивностью')

@shared_task
def send_course_update_notification(course_id):
    """Рассылка обновлений"""
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    for subscription in subscriptions:
        send_mail(
            f"Обновление курса {course.name}",
            "Курс обновлён, это может быть интересно!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=True,
        )