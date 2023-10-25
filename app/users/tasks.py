from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email(mail_subject, message, to):
    email = EmailMessage(mail_subject, message, to=to)
    if email.send():
        return True
    else:
        return False
