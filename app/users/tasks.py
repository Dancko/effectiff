from celery import shared_task
from verify_email.email_handler import send_verification_email


@shared_task
def complete_on_time(completed_tasks, expired_tasks):
    return 100 - expired_tasks // completed_tasks
