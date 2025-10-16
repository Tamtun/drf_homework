from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    threshold_date = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=threshold_date,
        is_active=True
    )

    count = inactive_users.update(is_active=False)
    print(f"Заблокировано пользователей: {count}")
