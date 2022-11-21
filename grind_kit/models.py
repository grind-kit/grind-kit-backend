from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class InstanceContent(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)
    # clear_exp = models.PositiveIntegerField(default=1)
    # clear_gil = models.PositiveIntegerField(default=1)
    # required_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)], null=True)