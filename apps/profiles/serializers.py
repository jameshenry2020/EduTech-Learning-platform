from rest_framework import serializers
from .models import UserProfile

class ProfileCreateSerializer(serializers.ModelSerializer):
    becomeTeacher=serializers.BooleanField(write_only=True)
    class Meta:
        model=UserProfile
        fields=['id', 'bio', 'occupation', 'becomeTeacher']

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        if validated_data.get('becomeTeacher') ==True:
            instance.user.is_instructor=True
            instance.user.save()
        instance.save()
        return instance

class UserProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avater']


class ProfileSerializer(serializers.ModelSerializer):
    names=serializers.CharField(source="user.names")
    email=serializers.EmailField(source='user.email')
    is_instructor=serializers.BooleanField(source='user.is_instructor')
    class Meta:
        model=UserProfile
        fields=['id','names', 'bio', 'occupation','email', 'avater', 'is_instructor']

