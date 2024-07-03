from django.urls import path
from . import views



urlpatterns=[
    path('update-profile', views.BecomeATeacher.as_view()),
    path('upload-photo', views.UploadProfilePhoto.as_view()),
    path('', views.GetUserProfile.as_view())
]