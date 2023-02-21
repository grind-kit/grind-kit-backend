from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User (AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class InstanceContent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
    clear_exp = models.PositiveIntegerField(default=1)
    clear_gil = models.PositiveIntegerField(default=1)
    required_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)


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
