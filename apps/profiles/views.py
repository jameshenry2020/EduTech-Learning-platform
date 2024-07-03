from rest_framework import generics, permissions, parsers, response, status
from .serializers import ProfileSerializer, ProfileCreateSerializer, UserProfilePictureSerializer
from .models import UserProfile
# Create your views here.

class BecomeATeacher(generics.GenericAPIView):
    serializer_class=ProfileCreateSerializer
    permission_classes=[permissions.IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        user_profile=UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(instance=user_profile, data=request.data,  partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UploadProfilePhoto(generics.UpdateAPIView):
    serializer_class=UserProfilePictureSerializer
    permission_classes=[permissions.IsAuthenticated]
    parser_classes=[parsers.MultiPartParser]
    queryset=UserProfile.objects.all()

    def get_object(self):
        return self.request.user.userprofile


class GetUserProfile(generics.RetrieveAPIView):
    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile



