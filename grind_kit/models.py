from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class InstanceContent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
    clear_exp = models.PositiveIntegerField(default=1)
    clear_gil = models.PositiveIntegerField(default=1)
    required_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    
class Job (models.Model):
    id = models.AutoField(primary_key=True)
    pld_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    war_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    drk_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    gnb_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    whm_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    sch_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    ast_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    sge_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    mnk_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    drg_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    nin_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    sam_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    rpr_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    brd_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    mch_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    dnc_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    blm_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    smn_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)
    rdm_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)

class Account (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firebase_uid = models.CharField(max_length=128)
    jobs_id = models.ForeignKey(Job, on_delete=models.CASCADE)

def __str__(self):
    return self.user.username