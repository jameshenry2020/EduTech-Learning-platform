from rest_framework import serializers
from .models import Category, Course


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'name', 'description']
    

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id', 'title', 'description', 'category', 'price', 'intro_vid', 'thumbnail', 'isPublished']
        extra_kwargs = {
            'description': {'required': False},
            'category': {'required': False},
            'price': {'required': False},
            'intro_vid': {'required': False},
            'thumbnail': {'required': False},
            'isPublished':{'required':False}
        }
