# services/notification_service.py

from apps.notifications.models import (
    Notification
)


class NotificationService:

    @staticmethod
    def create_notification(

        user,

        notification_type,

        title,

        message
    ):

        return Notification.objects.create(

            user=user,

            notification_type=notification_type,

            title=title,

            message=message,
        )
    



# services/email_service.py

from django.core.mail import (
    send_mail
)

from django.utils import timezone

from apps.notifications.models import (
    EmailNotification
)


class EmailService:

    @staticmethod
    def send_email(

        user,

        subject,

        message
    ):

        log = (
            EmailNotification.objects.create(

                user=user,

                email=user.email,

                subject=subject,
            )
        )

        try:

            send_mail(

                subject,

                message,

                None,

                [user.email],

                fail_silently=False,
            )

            log.status = "SENT"

            log.sent_at = (
                timezone.now()
            )

            log.save()

        except Exception as e:

            log.status = "FAILED"

            log.error_message = str(
                e
            )

            log.save()




# services/notification_service.py

from apps.notifications.tasks import (
    send_notification_email
)


class NotificationService:

    @staticmethod
    def notify(

        user,

        notification_type,

        title,

        message,

        send_email=False
    ):

        notification = (
            Notification.objects.create(

                user=user,

                notification_type=notification_type,

                title=title,

                message=message,
            )
        )

        if send_email:

            send_notification_email.delay(

                str(user.id),

                title,

                message,
            )

        return notification