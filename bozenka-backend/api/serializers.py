from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.sessions.models import Session
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Community, Tag, CommunityGrowth, CommunityER, Post, CommunityManager, LatestPostView, \
    SocialLink, CommunityConnection, Feature, FeatureSetting, Category


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_key', 'session_data', 'expire_date']


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

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError('Invalid username or password.')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'display_name', 'image', 'status')


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



class CommunityConnectionSerializer(serializers.ModelSerializer):
    """
    Serializer for connections between communities.
    """
    class Meta:
        model = CommunityConnection
        fields = ('platform', 'name', 'link', 'members_count', 'creation_date')


class PrivateCommunitySerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for categories of features.
    """
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "icon"
        )

class FeatureSerializer(serializers.ModelSerializer):
    """
    Serializer for features information.
    """
    category = CategorySerializer()
    class Meta:
        model = Feature
        fields = (
            "id",
            "name",
            "description",
            "enabled",
            "category",
        )

class FeatureSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for feature settings.
    """
    feature = FeatureSerializer()
    community = PrivateCommunitySerializer()
    class Meta:
        model = FeatureSetting
        fields = (
            "id",
            "community",
            "name",
            "description",
            "feature",
            "enabled",
            "settings_data"
        )


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
    user = UserSerializer()
    class Meta:
        model = CommunityManager
        fields = ('status', 'contact_link', 'avatar', 'user')


class LatestPostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestPostView
        fields = ('recording_date', 'views')


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ('platform', 'link')