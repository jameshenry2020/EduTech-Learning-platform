import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import MyUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    names = models.CharField(max_length=240, verbose_name=_("Names"))
    email = models.EmailField(max_length=255, verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_instructor=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.names
    
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["names"]
    
    objects = MyUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural=_("Users")

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
