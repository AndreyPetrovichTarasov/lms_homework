from datetime import timedelta
from django.utils.timezone import now
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, не заходивших более месяца.
    """
    one_month_ago = now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = users_to_deactivate.update(is_active=False)
    return f"{count} users deactivated."
