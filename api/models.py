from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class FirebaseUserManager(BaseUserManager):

    def create_user(self, uid, email, password=None, **extra_fields):
        if not uid:
            raise ValueError('The UID must be set')

        email = self.normalize_email(email)
        user = self.model(uid=uid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(uid, email, password, **extra_fields)


class FirebaseUser (AbstractUser, PermissionsMixin):
    uid = models.CharField(
        max_length=255, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    created = models.DateTimeField(default=timezone.now)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = FirebaseUserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Firebase User"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Bookmark (models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    instance_id = models.IntegerField(null=False, blank=False)
    value = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Bookmark"

    def __str__(self):
        return self.instance_id
