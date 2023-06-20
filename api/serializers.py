from rest_framework.serializers import ModelSerializer
from .models import InstanceContentBookmark, ContentFinderCondition

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


class InstanceContentBookmarkSerializer(ModelSerializer):
    class Meta:
        model = InstanceContentBookmark
        fields = [
            'id',
            'user',
            'content_finder_condition',
            'content_type_id',
            'value',
            'created_at',
            'updated_at',
        ]
