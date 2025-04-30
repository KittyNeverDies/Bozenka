"""
URL configuration for bozenka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import get_schema_view
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static


from api.views import PublicCommunityViews, TagViews, AuthViews, PrivateCommunityViews, AccountViews, \
    ServerStatusView

urlpatterns = [
    # Administration
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Get public information about communities and tags
    path('communities/', PublicCommunityViews.as_view({'get': 'list'}), name='communities'),
    path('communities/<str:community_id>/', PublicCommunityViews.as_view({'get': 'retrieve'}), name='community_detail'),
    path('tags/', TagViews.as_view({'get': 'list'}), name='tags'),

    # Authentication
    path('auth/register', AuthViews.as_view({'post': 'register'}), name='auth_register'),
    path('auth/login', AuthViews.as_view({'post': 'login'}), name='auth_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Private operations
    # Get users private communities
    path('private/communities/', PrivateCommunityViews.as_view({'get': 'communities'}), name='private_communities'),
    path('private/communities/<str:community_id>/', PrivateCommunityViews.as_view({'get': 'community'}), name='private_community_detail'),

    # Manage community
    path('private/communities/<str:community_id>/update/base', PrivateCommunityViews.as_view({'post': 'update_community_base_information'}),
         name='private_community_update'),
    path('private/communities/<str:community_id>/delete/',
         PrivateCommunityViews.as_view({'post': 'delete_community'}), name='private_community_delete'),
    path('private/communities/<str:community_id>/update/features/',
         PrivateCommunityViews.as_view({'post': 'edit_features'}), name='private_community_update_features'),
    path('privalte/communities/<str:community_id>/features/', PrivateCommunityViews.as_view({'get': 'get_list_of_features'}), name='private_community_features'),

    # Authenticated user operations
    path('private/user/account/', AccountViews.as_view({'get': 'account'}), name='private_user'),
    path('private/user/account/update', AccountViews.as_view({'post': 'update_account'}), name='private_user_update'),
    path('private/user/account/update_password', AccountViews.as_view({'post': 'update_password'}), name='private_user_password'),

    # Refresh access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Status view
    path('status/', ServerStatusView.as_view(), name='status_view'),

    # Schemas view
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    # Handle static files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.autodiscover()

