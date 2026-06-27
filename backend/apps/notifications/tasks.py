# tasks.py

from celery import shared_task

from django.contrib.auth import (
    get_user_model
)

from apps.notifications.services import EmailService



User = get_user_model()


@shared_task
def send_notification_email(

    user_id,

    subject,

    message
):

    user = User.objects.get(
        id=user_id
    )

    EmailService.send_email(

        user=user,

        subject=subject,

        message=message,
    )