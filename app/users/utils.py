from datetime import timedelta

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.timezone import make_aware

from .tokens import account_activation_token


def email_maker(request, user, to_email, email_template):
    message = render_to_string(
        str(email_template),
        {
            "user": user.name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.uuid)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    return message


def threshold_30(utc_now):
    delta = timedelta(days=30)
    threshold = make_aware(utc_now - delta)
    return threshold
