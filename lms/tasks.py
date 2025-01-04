from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_course_update_email(user_email, course_name, update_info):
    """
    Отправка уведомления об обновлении курса.
    """
    subject = f"Обновление курса: {course_name}"
    message = f"Здравствуйте! Курс '{course_name}' был обновлен. Подробнее: {update_info}."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
