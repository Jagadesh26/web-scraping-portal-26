from celery import shared_task

from apps.accounts.models import User


@shared_task
def send_verification_email_task(
    user_id
):

    from apps.accounts.services.auth_service import (
        AuthService
    )

    try:

        user = User.objects.get(
            id=user_id
        )

        AuthService.send_verification_email(
            user
        )

    except User.DoesNotExist:

        pass



@shared_task
def send_password_reset_email_task(
    user_id
):

    from apps.accounts.services.auth_service import (
        AuthService
    )

    try:

        user = User.objects.get(
            id=user_id
        )

        AuthService.send_password_reset_email(
            user
        )

    except User.DoesNotExist:

        pass