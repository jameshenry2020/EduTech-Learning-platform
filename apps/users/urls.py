from django.urls import path

from . import views


urlpatterns=[
    path('signup', views.CustomUserSignUpEndpoint.as_view()),
    path('jwt/login', views.CustomTokenObtainView.as_view()),
    path('jwt/verify', views.CustomTokenVerifyView.as_view()),
    path('jwt/refresh', views.CustomTokenRefreshView.as_view()),
    path('google/signin', views.GoogleOauthSignInview.as_view()),
    path('activation/<str:uidb64>/<str:token>', views.EmailAccountActivationView.as_view(), name="email_activation"),
    path('logout', views.LogoutEndpointView.as_view()),
    path('forget-password/', views.ForgetPasswordRequest.as_view(), name='forget-password'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('reset-password/', views.SetNewPasswordView.as_view(), name='reset-password'),
]