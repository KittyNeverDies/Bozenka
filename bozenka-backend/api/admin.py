from django.contrib import admin

from .models import (
    User, Tag, Community, CommunityGrowth, CommunityER, Post,
    CommunityManager, SocialLink, LatestPostView
)

# Register your models here
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Community)
admin.site.register(CommunityGrowth)
admin.site.register(CommunityER)
admin.site.register(Post)
admin.site.register(CommunityManager)
admin.site.register(SocialLink)
admin.site.register(LatestPostView)