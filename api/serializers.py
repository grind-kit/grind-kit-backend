from rest_framework.serializers import ModelSerializer
from .models import FirebaseUser, Bookmark, ContentFinderCondition


class FirebaseUserSerializer(ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = ['username', 'lodestone_id']

    def create(self, validated_data):
        user = FirebaseUser.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )
        user.save()
        return user

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