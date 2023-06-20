from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from firebase_admin import auth

class FirebaseUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The UID must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        # Check if a user with this email already exists
        if FirebaseUser.objects.filter(email=email).exists():
            raise ValueError('A user with this email already exists')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class FirebaseUser (AbstractUser, PermissionsMixin):
    username = models.CharField(
        max_length=255, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True, blank=True)
    lodestone_id = models.IntegerField(default=None, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = FirebaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Firebase User"
        verbose_name_plural = "Firebase Users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class FirebaseUserToken (models.Model):
    user = models.OneToOneField(FirebaseUser, on_delete=models.CASCADE)
    id_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Firebase User Token"
        verbose_name_plural = "Firebase User Tokens"
