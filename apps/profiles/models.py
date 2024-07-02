from django.db import models
from apps.users.models import CustomUser
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    avater = models.ImageField(upload_to="profiles", null=True, blank=True)
    wallet = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)


    def __str__(self) -> str:
        return self.user.names