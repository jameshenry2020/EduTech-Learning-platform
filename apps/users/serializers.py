from .models import CustomUser
from rest_framework import serializers, exceptions
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from .google import Google, register_google_user
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import send_reset_password_email
from django.utils.encoding import  force_str

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2= serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model=CustomUser
        fields = ['id','email', 'names', 'password', 'password2']

    def validate(self, attrs):
        password=attrs.get('password', '')
        password2 =attrs.get('password2', '')
        if password !=password2:
            raise serializers.ValidationError("passwords do not match")
        if CustomUser.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("email already in use!")
        return attrs

    def create(self, validated_data):
        user= CustomUser.objects.create_user(
            email=validated_data['email'],
            names=validated_data.get('names'), 
            password=validated_data.get('password')
            )
        return user


class GoogleUserSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        user_data=Google.validate(access_token)
        try:
            userid=user_data['sub']
            email=user_data['email']
            first_name=user_data['given_name']
            last_name=user_data['family_name']
            names=f"{first_name} {last_name}"
            provider='google'
        except:
            raise exceptions.AuthenticationFailed(detail="token is invalid or has expired")
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise exceptions.AuthenticationFailed('Could not verify user.')
        return register_google_user(provider, email, names)
        

    

class ForgetPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255, min_length=10)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(detail="link to reset your password has been sent!")
        user= CustomUser.objects.get(email=email)
        send_reset_password_email(user, {'request':self.context.get('request')})
        return super().validate(attrs)
    

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(pkid=user_id)
            if not default_token_generator.check_token(user, token):
                raise exceptions.AuthenticationFailed("reset link is invalid or has expired", 401)
            if password != confirm_password:
                raise exceptions.AuthenticationFailed("passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return exceptions.AuthenticationFailed("link is invalid or has expired")


    