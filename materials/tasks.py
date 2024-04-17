from datetime import datetime, timedelta
from config import settings
from materials.models import Subscription
from celery import shared_task
from django.core.mail import send_mail
from users.models import User
import logging


@shared_task
def check_subscribe_course(course_pk):
    course_subscriptions= Subscription.objects.filter(course_id=course_pk)
    recipient_email = []
    for subscription in course_subscriptions:

        if subscription.status_subscrip:
            recipient_email.append(subscription.user.email)

    send_mail(
        subject="Обновление курса",
        message="Курс на который вы подписаны обновлен",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_email,
        fail_silently=False
        )

@shared_task
def deactivate_user():
    thirty_days_ago = datetime.now() - timedelta(days=30)

    users = User.objects.filter(
        last_login__lt=thirty_days_ago,
        is_staff=False,
        is_superuser=False
    )

    for user in users:
        logging.info(f'Пользователь {user} заблокирован')
    users.update(is_active=False)
