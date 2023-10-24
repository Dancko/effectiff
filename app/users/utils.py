from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import account_activation_token
from .tasks import send_email


def activate_email(request, user, to_email):
    mail_subject = "Email Verification Mail"
    message = render_to_string(
        "users/activate_account.html",
        {
            "user": user.name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.uuid)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    send_email.delay(mail_subject, message, to=[to_email])
