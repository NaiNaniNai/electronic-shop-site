from django.conf import settings
from django.core.mail import send_mail

from project_root.celery import app


@app.task
def send_email_task(title, message, email):
    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [
            email,
        ],
    )
