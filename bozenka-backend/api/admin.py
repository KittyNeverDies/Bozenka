from django.contrib import admin

from .models import (
    User, Tag, Community, CommunityGrowth, CommunityER, Post,
    CommunityManager, SocialLink, LatestPostView, CommunityConnection
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
admin.site.register(CommunityConnection)

admin.site.site_title = 'Bozenka Admin Panel'
admin.site.site_header = 'Bozenka Admin Panel'
admin.site.index_title = 'Manage things, what you need, administrator.'
admin.site.enable_nav_sidebar = True
