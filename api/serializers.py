from rest_framework.serializers import ModelSerializer
from .models import FirebaseUser


class FirebaseUserSerializer(ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = [
            "uid",
            "email",
            "password"
        ]

    def create(self, validated_data):
        user = FirebaseUser.objects.create_user(
            validated_data["uid"],
            validated_data["email"],
            validated_data["password"]
        )
        user.save()
        return user
