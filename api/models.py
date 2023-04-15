from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
    created = models.DateTimeField(default=timezone.now)
    lodestone_id = models.IntegerField(null=True, default=None)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = FirebaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Firebase User"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class ContentFinderCondition (models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=True)
    class_job_level_required = models.IntegerField(null=False, blank=False)
    item_level_required = models.IntegerField(null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)
    content_type_id = models.IntegerField(null=False, blank=False)
    accept_class_job_category = models.JSONField(null=False, blank=False)

class Bookmark (models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    instance_id = models.IntegerField(null=False, blank=False)
    value = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Bookmark"

    def __str__(self):
        return self.instance_id
