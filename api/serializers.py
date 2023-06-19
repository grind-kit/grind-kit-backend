from rest_framework.serializers import ModelSerializer
from .models import FirebaseUser, FirebaseUserToken, InstanceContentBookmark, ContentFinderCondition


class FirebaseUserSerializer(ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = ['id', 'username', 'lodestone_id']

    def create(self, validated_data):
        user = FirebaseUser.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )
        user.save()
        return user


class FirebaseUserTokenSerializer(ModelSerializer):
    class Meta:
        model = FirebaseUserToken
        fields = ['id', 'user', 'id_token',
                  'refresh_token', 'created_at', 'updated_at']


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
