from uuid import UUID

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Community, Tag, CommunityGrowth, CommunityER, CommunityManager, SocialLink, Post, LatestPostView
from .serializers import RegisterSerializer, LoginSerializer, PublicCommunitySerializer, TagSerializer, \
    CommunityGrowthSerializer, CommunityERSerializer, CommunityManagerSerializer, PostSerializer, SocialLinkSerializer, \
    LatestPostViewSerializer, UserSerializer


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

        # Get the email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        # Create a new user using the register serialzier
        serializer = RegisterSerializer(data={'email': email, 'password': password, 'username': username})

        if serializer.is_valid():
            # Generating refresh and access tokens for the user
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            # Return the response with the refresh and access tokens
            return Response({'message':
                                 'Successfully registered.',
                                    'refresh_token': str(refresh),
                                    'access_token': str(refresh.access_token)},
                            status=status.HTTP_201_CREATED)

        # Handle errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login(self, request) -> Response:
        """
        View for logging in a user
        :param request: Request object
        :return: Response object
        """

        username = request.data.get('username')
        password = request.data.get('password')
        serializer = LoginSerializer(data={'username': username, 'password': password})

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return Response({'message':
                                 'Successfully logged in.',
                             'refresh_token': str(refresh),
                             'access_token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountViews(viewsets.ModelViewSet):
    """
    ViewsSet for accessing user account information of bozenka platform.
    Gives ability to get information about user with authentication.
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def account(self, request) -> Response:
        """
        View for getting user information
        :param request: Request object
        :return: Response object
        """
        user = request.user

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_account(self, request):
        """
        View for updating user information
        :param request: Request object
        :return: Response object
        """
        user = request.user

        try:
            updated_data = request.data

            if 'id' in updated_data.keys():
                return Response("You can't change your id.", status=status.HTTP_400_BAD_REQUEST)

            UserSerializer(user, data=updated_data, partial=True).is_valid(raise_exception=True)
            UserSerializer(user, data=updated_data, partial=True).save()

            return Response({'message': 'Successfully updated.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': 'Failed to update.', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_accounts(self, request):
        """
        View for updating user information
        :param request: Request object
        :return: Response object
        """
        user = request.user

        password = request.data.get('password')

        try:
            if LoginSerializer(data={'username': user.username, 'password': password}).is_valid():
                user.password = request.data.get('new_password')
                user.save()
                return Response({'message': 'Successfully updated.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to update.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'Failed to update. Exception happend.'}, status=status.HTTP_400_BAD_REQUEST)



def is_valid_uuid(uuid_to_test: str, version: int = 4) -> bool:
    """
    Check is uuid valid
    :param uuid_to_test: string UUID to test
    :param version: Version of UUID
    :return: Boolean value
    >>> is_valid_uuid('12345678-1234-5678-1234-567812345678')
    True
    >>> is_valid_uuid('invalid-uuid')
    False
    >>> is_valid_uuid('12345678-1234-1234-1234-567812345678', version=1)
    False
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
        return True
    except ValueError:
        return False

class UserViews(viewsets.ViewSet):
    """
    ViewsSet for accessing user of bozenka platform.
    Gives ability to get information about user without authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

class PrivateCommunityViews(viewsets.ViewSet):
    """
    ViewsSet for accessing communities of bozenka platform.
    Gives ability to get information about communities with authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def communities(self, request) -> Response:
        """
        View for getting all communities
        with ability to edit.
        :param request: Request object
        :return: Response object
        """
        user = request.user
        managers_roles = CommunityManager.objects.filter(user=user)
        communities = [PublicCommunitySerializer(manager_role.community) for manager_role in managers_roles]

        return Response(communities, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_community_base_information(self, request, community_id=None) -> Response | None:
        """
        View for updating community
        :param request: Request object
        :return: Response object
        """
        user = request.user

        if community_id is None or is_valid_uuid(community_id):
            return Response({'message': 'Community id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not Community.objects.filter(id=community_id).exists():
            return Response({'message': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        community = Community.objects.get(id=community_id)
        managers_roles = CommunityManager.objects.filter(user=user, community=community)

        if not managers_roles.exists():
            return Response({'message': 'You are not a manager of this community.'}, status=status.HTTP_403_FORBIDDEN)

        # Get data, what we need update from request
        updated_data = request.data.get('updated_data')

        if "id" in updated_data.keys():
            return Response({'message': 'You can not change community id.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update community information
        for key, value in updated_data.items():
            setattr(community, key, value)

        community.save()

        return Response({'message': 'Community updated successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def delete_community(self, request, community_id) -> Response:
        """
        View for deleting community
        :param request: Request object
        :param community_id: Community id
        :return: Response object
        """
        user = request.user

        if community_id is None or is_valid_uuid(community_id):
            return Response({'message': 'Community id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not Community.objects.filter(id=community_id).exists():
            return Response({'message': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        community = Community.objects.get(id=community_id)
        managers_roles = CommunityManager.objects.filter(user=user, community=community)

        if not managers_roles.exists():
            return Response({'message': 'You are not a manager of this community.'}, status=status.HTTP_403_FORBIDDEN)

        if managers_roles[0].status != 'owner':
            return Response({'message': 'You are not an owner of this community.'}, status=status.HTTP_403_FORBIDDEN)

        community.delete()

        return Response({'message': 'Community deleted successfully.'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def edit_enabled_features(self, request, community_id=None):
        """
        View for editing enabled features of community
        :param request: Request object
        :param community_id: Community id
        :return: Response object
        """
        pass

    # More features will be added here


class PublicCommunityViews(viewsets.ViewSet):
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
        serializer = PublicCommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def retrieve(self, request, community_id=None) -> Response:
        """
        View for getting a community by its id
        :param request: Request object
        :param community_id: Community id
        :return: Response object
        """
        print(community_id)

        # Validation of community_id parameter
        if community_id is None or not is_valid_uuid(community_id):
            return Response({'message': 'Community id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not Community.objects.filter(id=community_id).exists():
            return Response({'message': 'Community not found.'}, status=status.HTTP_404_NOT_FOUND)

        community = Community.objects.get(id=community_id)

        # Get all data about community to show it.
        growth_stats = CommunityGrowth.objects.filter(community=community).order_by('-date')
        er_stats = CommunityER.objects.filter(community=community).order_by('-date')
        managers = CommunityManager.objects.filter(community=community)
        social_links = SocialLink.objects.filter(community=community)
        posts = Post.objects.filter(community=community).order_by('-created_at')
        latest_post_views = LatestPostView.objects.filter(community=community, post=posts[0]) if posts else []

        # Format data for response
        growth_data = [CommunityGrowthSerializer(stat).data for stat in growth_stats]
        er_data = [CommunityERSerializer(stat).data for stat in er_stats]
        managers_data = [CommunityManagerSerializer(manager).data for manager in managers]
        social_links_data = [SocialLinkSerializer(social_link).data for social_link in social_links]
        posts_data = [PostSerializer(post).data for post in posts]
        latest_post_views_data = [LatestPostViewSerializer(latest_post_view).data
                                  for latest_post_view in latest_post_views]

        serializer = PublicCommunitySerializer(community)
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

