from rest_framework import serializers
from .models import FirebaseUser, FirebaseUserToken


class FirebaseUserSerializer(serializers.ModelSerializer):
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


class FirebaseUserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUserToken
        fields = ['id', 'user', 'id_token',
                  'refresh_token', 'created_at', 'updated_at']
