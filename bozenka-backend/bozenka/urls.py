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
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static


from api.views import PublicCommunityViews, TagViews, AuthViews, PrivateCommunityViews, AccountViews

urlpatterns = [
    # Administration
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Get public information about communities and tags
    path('communities/', PublicCommunityViews.as_view({'get': 'list'}), name='communities'),
    path('communities/<str:community_id>/', PublicCommunityViews.as_view({'get': 'retrieve'}), name='community_detail'),
    path('tags/', TagViews.as_view({'get': 'list'}), name='tags'),
    path('private/communities/', PrivateCommunityViews.as_view({'get': 'communities'}), name='private_communities'),
    path('private/communities/<str:community_id>/', PrivateCommunityViews.as_view({'get': 'community'}), name='private_community_detail'),
    path('private/communities/<str:community_id>/update/base', PrivateCommunityViews.as_view({'post': 'update_community_base_information'}),
         name='private_community_update'),
    path('private/communities/<str:community_id>/delete/',
         PrivateCommunityViews.as_view({'post': 'delete_community'}), name='private_community_delete'),

    # Authenticated user operations
    path('private/user/account/', AccountViews.as_view({'get': 'account'}), name='private_user'),
    path('private/user/account/update', AccountViews.as_view({'post': 'update_accounr'}), name='private_user_update'),
    path('private/user/account/update_password', AccountViews.as_view({'post': 'update_password'}), name='private_user_password'),

    # Authentication
    path('auth/register', AuthViews.as_view({'post': 'register'}), name='auth_register'),
    path('auth/login', AuthViews.as_view({'post': 'login'}), name='auth_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.autodiscover()

