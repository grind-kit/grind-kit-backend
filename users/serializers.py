from rest_framework import serializers
from .models import *


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


class UserBookmarkGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookmark
        fields = [
            'id',
            'user_id',
            'content_finder_condition_id',
            'content_type_id',
            'value',
            'created_at',
            'updated_at',
        ]

class UserBookmarkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookmark
        fields = [
            'value',
            'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = [
            'id',
            'username',
            'lodestone_id',
            'created_at',
            'updated_at',
        ]