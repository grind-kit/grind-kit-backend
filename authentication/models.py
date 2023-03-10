from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser (AbstractUser, PermissionsMixin):
    userId = models.CharField(
        max_length=255, default=uuid4, primary_key=True, editable=False)
    username = models.CharField(
        max_length=255, unique=True)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Custom User"

    def __str__(self):
        return self.email


class InstanceContent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
    clear_exp = models.PositiveIntegerField(default=1)
    clear_gil = models.PositiveIntegerField(default=1)
    required_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    
    def __str__(self):
        return self.name


class Job (models.Model):
    id = models.AutoField(primary_key=True)
    pld_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    war_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    drk_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    gnb_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    whm_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    sch_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    ast_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    sge_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    mnk_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    drg_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    nin_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    sam_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    rpr_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    brd_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    mch_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    dnc_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    blm_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    smn_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    rdm_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    
    def __str__(self):
        return self.id
