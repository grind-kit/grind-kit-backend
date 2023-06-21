from rest_framework.serializers import ModelSerializer
from .models import ContentFinderCondition

class ContentFinderConditionSerializer(ModelSerializer):
    class Meta:
        model = ContentFinderCondition
        fields = [
            'id',
            'name',
            'class_job_level_required',
            'item_level_required',
            'url',
            'content_type_id',
            'accept_class_job_category',
        ]