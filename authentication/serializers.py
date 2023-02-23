from rest_framework.serializers import ModelSerializer
from .models import CustomUserModel, InstanceContent, Job
from django.conf import settings


class CustomUserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = [
            "userId",
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        user = CustomUserModel.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )

        return user


class InstanceContentSerializer(ModelSerializer):
    class Meta:
        model = InstanceContent
        fields = '__all__'


class JobsSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
