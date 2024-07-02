from django.conf import settings 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions, status, exceptions
from .models import CustomUser
from .serializers import  UserCreateSerializer, GoogleUserSignInSerializer, ForgetPasswordSerializer, SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,DjangoUnicodeDecodeError
from .utils import send_activation_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# Create your views here.

class CustomUserSignUpEndpoint(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class=UserCreateSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            send_activation_email(user, {'request':request})
            response =  Response(serializer.data, status=status.HTTP_201_CREATED)
            if response.status_code == status.HTTP_201_CREATED:  
                refresh = RefreshToken.for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=str(refresh.access_token),
                    max_age=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS_MAX_AGE'],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=str(refresh),
                    max_age=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH_MAX_AGE'],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailAccountActivationView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        uid=kwargs.get('uidb64')
        token=kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise exceptions.ValidationError("Invalid uid or user does not exist")
        if not default_token_generator.check_token(user, token): 
            raise exceptions.ValidationError("Invalid token or token has expired")
        user.is_verified=True
        user.save()
        return Response({'message':"account verified successfully"}, status=status.HTTP_204_NO_CONTENT)
              

class CustomTokenObtainView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                max_age=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS_MAX_AGE'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=refresh_token,
                max_age=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH_MAX_AGE'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) -> Response:
        refresh_token=request.COOKIES.get('jwt_refresh')
        if refresh_token:
            request.data['refresh']=refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                max_age=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS_MAX_AGE'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )            

        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get('jwt_access')
        if access_token:
            request.data['token']=access_token
        return super().post(request, *args, **kwargs)
    

class LogoutEndpointView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('jwt_access')
        response.delete_cookie('jwt_refresh')

        return response
    
class ForgetPasswordRequest(generics.GenericAPIView):
    serializer_class=ForgetPasswordSerializer
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    
class PasswordResetConfirm(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(pkid=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"password reset is succesful"}, status=status.HTTP_200_OK)



class GoogleOauthSignInview(generics.GenericAPIView):
    serializer_class=GoogleUserSignInSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=((serializer.validated_data)['access_token'])
        response = Response(data, status=status.HTTP_200_OK)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                max_age=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS_MAX_AGE'],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=refresh_token,
                max_age=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH_MAX_AGE'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTPONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            return response 
