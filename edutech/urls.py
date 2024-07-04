from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from apps.courses.views import CategoryEndpoint, CourseCrudEndpoint


router=DefaultRouter()
router.register(r'category', CategoryEndpoint)
router.register(r'host', CourseCrudEndpoint)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include("apps.users.urls")),
    path('api/profile/', include('apps.profiles.urls')),
    path('api/course/', include(router.urls))
  
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
