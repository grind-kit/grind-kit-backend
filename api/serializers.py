from rest_framework.serializers import ModelSerializer
from .models import FirebaseUser


class FirebaseUserSerializer(ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = [
            "username",
            "email",
            "password",
            "lodestone_id"
        ]

    def create(self, validated_data):
        user = FirebaseUser.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )
        user.save()
        return user
