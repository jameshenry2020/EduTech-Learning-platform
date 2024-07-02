from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .models import CustomUser
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site



def send_activation_email(user:CustomUser, content):
    uid=urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    url=reverse('email_activation', kwargs={'uidb64':uid, 'token':token})
    context={
        'protocol':'http',
        'domain':get_current_site(content.get('request')).domain,
        'url':url,
        'site_name':settings.SITE_NAME
    }
    email_subject=f"Email Verification for {settings.SITE_NAME}"
    email_html_message = render_to_string('email_template.html', context)
    send_email(email_html_message, email_subject, user)

def send_reset_password_email(user:CustomUser, content):
    uidb64=urlsafe_base64_encode(force_bytes(user.pkid))
    token = default_token_generator.make_token(user)
    request=content.get('request')
    current_site=get_current_site(request).domain
    relative_link =reverse('reset-password-confirm', kwargs={'uidb64':uidb64, 'token':token})

    context={
        'protocol':'http',
        'domain':current_site,
        'url':relative_link,
        'site_name':settings.SITE_NAME
    }
    email_subject=f"Password Reset Request"
    email_html_message = render_to_string('email_reset.html', context)
    send_email(email_subject, email_html_message,  user)


def send_email(subject, html_message, user=None ):
    email = EmailMessage(
                subject.replace('\n', '').replace('\r', ''),
                html_message,
                settings.DEFAULT_FROM_EMAIL,  # from email
                [user.email]  # to email
            )
    email.content_subtype = "html" 
    email.send()
