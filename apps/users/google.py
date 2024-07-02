from google.auth.transport import requests
from google.oauth2 import id_token
from .models import CustomUser
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except:
            return "the token is either invalid or has expired"
        

def google_jwt_login(email, password):
    user = authenticate(email=email, password=password)
    user_token= RefreshToken.for_user(user)
    return {
        "refresh":str(user_token),
        "access":str(user_token.access_token)
    }


def register_google_user(provider, email, names):
    user = CustomUser.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            login_user=google_jwt_login(email, settings.SERVER_PASSWORD)
        else:
            raise AuthenticationFailed(detail=f"please continue your login with {user[0].auth_provider}")
    else:
        new_user={
            'names':names,
            'email':email,
            'password':settings.SERVER_PASSWORD
        }
        user = CustomUser.objects.create_user(**new_user)
        user.is_verified=True
        user.auth_provider=provider
        user.save()
        login_user= google_jwt_login(user.email, password=settings.SERVER_PASSWORD)
    return login_user

