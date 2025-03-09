from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Community, Tag, CommunityGrowth, CommunityER, Post, CommunityManager, LatestPostView, \
    SocialLink



class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data = data

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data) -> User:
        """
        Creates a new user.
        :param validated_data: A valid date for creating a user.
        :return:
        """
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in a user.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data) -> AbstractBaseUser:
        """
        Validates the login data.
        :param data: The login data.
        :return: The validated data.
        """

        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise ValidationError('Invalid username or password.')
        return user


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tags.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'icon')


class PublicCommunitySerializer(serializers.ModelSerializer):
    """
    Serializer for public information about communities.
    """
    tags = TagSerializer(many=True)
    class Meta:
        model = Community
        fields = ('id', 'name',
                  'description',
                  'short_description',
                  'creation_date',
                  'tags', 'icon', 'members_count')


    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.url
        return None


class PrivateCommunitySerializer(serializers.ModelSerializer):
    pass





class CommunityGrowthSerializer(serializers.ModelSerializer):
    """
    Serializer for community growth.
    """
    class Meta:
        model = CommunityGrowth
        fields = (
            'community',
            'members_count',
            'growth',
            'date'
        )


class CommunityERSerializer(serializers.ModelSerializer):
    """
    Serializer for community growth.
    """
    class Meta:
        model = CommunityER
        fields = (
            'community',
            'er',
            'date'
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', 'source', 'created_at', 'views')


class CommunityManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityManager
        fields = ('status', 'contact_link', 'avatar')


class LatestPostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestPostView
        fields = ('recording_date', 'views')


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ('platform', 'link')