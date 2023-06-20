from django.db import models
from django.utils import timezone
from ..users.models import FirebaseUser


class ContentFinderCondition (models.Model):
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=True)
    class_job_level_required = models.IntegerField(null=False, blank=False)
    item_level_required = models.IntegerField(null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)
    content_type_id = models.IntegerField(null=True, blank=False)
    accept_class_job_category = models.JSONField(null=True, blank=False)

    class Meta:
        verbose_name = "Content Finder Condition"

    def __str__(self):
        return str(self.id) + " - " + self.name


class InstanceContentBookmark (models.Model):
    user = models.ForeignKey(FirebaseUser, on_delete=models.CASCADE)
    content_finder_condition = models.ForeignKey(
        ContentFinderCondition, on_delete=models.CASCADE)
    content_type_id = models.IntegerField(null=True, blank=False)
    value = models.IntegerField(null=False, blank=False, default=1)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Instance Content Bookmark"
        unique_together = ('user', 'content_finder_condition')

    def __str__(self):
        return str(self.id) + " - " + self.content_finder_condition.name
