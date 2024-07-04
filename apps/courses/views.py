from django.shortcuts import render
from rest_framework import viewsets, status, permissions, response
from apps.users.permissions import IsTeacherUser
from .serializers import CourseCategorySerializer, CourseCreateSerializer
from .models import Category, Course
from rest_framework.decorators import action
# Create your views here.


class CategoryEndpoint(viewsets.ModelViewSet):
    serializer_class=CourseCategorySerializer
    queryset=Category.objects.all()

    @action(detail=True, methods=['put'], url_path="update")
    def update_category(self, request, pk=None):
        category = self.get_object()
        serializer = CourseCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    

#for instructors only
class CourseCrudEndpoint(viewsets.ModelViewSet):
    serializer_class=CourseCreateSerializer
    queryset=Course.objects.all()
    permission_classes=[IsTeacherUser]

    def get_queryset(self):
        queryset= super().get_queryset()
        return queryset.filter(instructor=self.request.user)
    
    def get_object(self):
        obj = super().get_object()
        if self.action in ['update_course', 'destroy']:
            self.check_object_permissions(self.request, obj)
        return obj
    
     
    @action(detail=False, methods=['post'], url_path="create-course")
    def create_course(self, request):
        serializer=CourseCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(instructor=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['put'], url_path='update-course')
    def update_course(self, request, pk=None):
        course = self.get_object()
        serializer = CourseCreateSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
