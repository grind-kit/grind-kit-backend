from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, uid, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(uid=uid, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, uid, email, password):
        user = self.create_user(
            uid,
            email,
            password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class FirebaseUser (AbstractUser, PermissionsMixin):
    uid = models.CharField(
        max_length=255, unique=True)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Firebase User"

    def __str__(self):
        return self.email
    

class Bookmarks(models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    instance_id = models.IntegerField(null=False, blank=False)
    value = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.instance_id