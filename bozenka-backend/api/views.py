from uuid import UUID

from django.contrib.auth import login

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Community, Tag, CommunityGrowth, CommunityER, CommunityManager, SocialLink, Post, LatestPostView
from .serializers import RegisterSerializer, LoginSerializer, CommunitySerializer, TagSerializer, \
    CommunityGrowthSerializer, CommunityERSerializer, CommunityManagerSerializer, PostSerializer, SocialLinkSerializer, \
    LatestPostViewSerializer


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

class AuthViews(viewsets.ViewSet):
    """
    ViewsSet for authentication of bozenka platform.
    Gives ability to access to accounts using email and password
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request) -> Response:
        """
        View for registering a new user
        :param request: Request object
        :return: Response object
        """
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = RegisterSerializer(data={'email': email, 'password': password})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Successfully registered.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login(self, request) -> Response:
        """
        View for logging in a user
        :param request: Request object
        :return: Response object
        """
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = LoginSerializer(data={'email': email, 'password': password})
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({'message': 'Successfully logged in.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityViews(viewsets.ViewSet):
    """
    ViewsSet for accessing communities of bozenka platform.
    Gives ability to get information about communities without authentication.
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def list(self, request) -> Response:
        """
        View for getting all communities
        :param request: Request object
        :return: Response object
        """
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def retrieve(self, request, community_id=None) -> Response:
        """
        View for getting a community by its id
        :param request: Request object
        :param community_id: Community id
        :return: Response object
        """

        # Validation of community_id parameter
        if community_id is None or is_valid_uuid(community_id):
            return Response({'message': 'Community id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Community.objects.filter(id=community_id).exists():
            return Response({'message': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        community = Community.objects.get(id=community_id)

        # Get all data about community to show it.
        growth_stats = CommunityGrowth.objects.filter(community=community).order_by('-date')
        er_stats = CommunityER.objects.filter(community=community).order_by('-date')
        managers = CommunityManager.objects.filter(community=community)
        social_links = SocialLink.objects.filter(community=community)
        posts = Post.objects.filter(community=community).order_by('-created_at')
        latest_post_views = LatestPostView.objects.filter(community=community, post=posts[0]) if posts else []


        growth_data = [CommunityGrowthSerializer(stat).data for stat in growth_stats]
        er_data = [CommunityERSerializer(stat).data for stat in er_stats]
        managers_data = [CommunityManagerSerializer(manager).data for manager in managers]
        social_links_data = [SocialLinkSerializer(social_link).data for social_link in social_links]
        posts_data = [PostSerializer(post).data for post in posts]
        latest_post_views_data = [LatestPostViewSerializer(latest_post_view).data
                                  for latest_post_view in latest_post_views]

        serializer = CommunitySerializer(community)
        community_data = {
            'community_info': serializer.data,
            'growth_stats': growth_data,
            'er_stats': er_data,
            'managers': managers_data,
            'social_links': social_links_data,
            'posts': posts_data,
            'latest_post_views': latest_post_views_data

        }

        return Response(community_data, status=status.HTTP_200_OK)


class TagViews(viewsets.ViewSet):
    """
    ViewsSet for accessing tags of bozenka platform.
    Gives ability to access to list of tags without authentication.
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def list(self, request) -> Response:
        """
        View for getting all tags
        :param request: Request object
        :return: Response object
        """
        communities = Tag.objects.all()
        serializer = TagSerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

