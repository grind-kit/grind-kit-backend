from rest_framework.serializers import ModelSerializer
from .models import FirebaseUser


class UserSerializer(ModelSerializer):
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

        return user
