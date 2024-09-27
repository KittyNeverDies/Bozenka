from django.contrib import admin


from .models import *


admin.site.register(Tag)


admin.site.register(Community)
admin.site.register(CommunityER)
admin.site.register(CommunityManager)
admin.site.register(CommunityGrowth)
admin.site.register(LatestPostView)
admin.site.register(SocialLink)
admin.site.register(Post)
