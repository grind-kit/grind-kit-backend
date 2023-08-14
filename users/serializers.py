from rest_framework import serializers
from .models import *


class FirebaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = ['id', 'username', 'email', 'lodestone_id',
                  'created_at', 'updated_at', 'password']

    def create(self, validated_data):
        user = FirebaseUser.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )
        user.save()
        return user


class FirebaseUserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = ['id', 'lodestone_id', 'updated_at']


class FirebaseUserTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUserToken
        fields = ['id', 'user', 'id_token',
                  'refresh_token', 'created_at', 'updated_at']


class FirebaseUserTokenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUserToken
        fields = ['id', 'user', 'id_token', 'updated_at']


class UserBookmarkRetrieveSerializer(serializers.ModelSerializer):
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

class UserBookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookmark
        fields = [
            'id',
            'user_id',
            'content_type_id',
            'content_finder_condition_id',
            'value',
        ]
    
    def create(self, validated_data):
        bookmark = UserBookmark.objects.create(
            user_id=validated_data["user_id"],
            content_type_id=validated_data["content_type_id"],
            content_finder_condition_id=validated_data["content_finder_condition_id"],
            value=validated_data["value"],
        )
        bookmark.save()
        return bookmark


class UserBookmarkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookmark
        fields = [
            'id',
            'value',
            'updated_at'
        ]
