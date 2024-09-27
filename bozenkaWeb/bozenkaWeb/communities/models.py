from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """
    A tag associated with a community
    """
    name = models.CharField(
        verbose_name=_("Name of tag"),
        max_length=50,
        unique=True)
    icon = models.CharField(
        verbose_name=_("Icon of Tag"),
        max_length=50,
        unique=False,
        default="sell"
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Community(models.Model):
    """
    A community with its description, creation date, tags, icon, and member count
    """

    name = models.TextField(
        verbose_name=_("Name of Community")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default=_("No description provided")
    )
    short_description = models.TextField(
        verbose_name=_("Short Description"),
        max_length=100,
        default=_("No short description provided"),
    )
    creation_date = models.DateTimeField(
        verbose_name=_("Creation date"),
        auto_now_add=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags")
    )

    icon = models.ImageField(
        upload_to='images/community_icons',
        verbose_name=_("Icon")
    )

    members_count = models.IntegerField(
        default=0,
        verbose_name=_("Count of Members")
    )

    class Meta:
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")


class CommunityGrowth(models.Model):
    """
    Community growth data for a specific period (month, week, day)
    """
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name=_("Community")
    )
    members_count = models.IntegerField(
        default=0,
        verbose_name=_("Count of Members")
    )
    growth = models.IntegerField(
        verbose_name=_("Growth of Members")
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of Recording")
    )

    class Meta:
        verbose_name = _("Community growth record")
        verbose_name_plural = _("Community growth records")


class CommunityER(models.Model):
    """
    Community engagement rate data for a specific period (month, week, day)
    """
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name=_("Community")
    )
    er = models.DecimalField(max_digits=5, decimal_places=2,
                             verbose_name="ER")
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of Recording")
    )

    class Meta:
        verbose_name = _("ER growth record")
        verbose_name_plural = _("ER growth records")


class Post(models.Model):
    """
    A post in a community with its text, source, views, and creation date
    """
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name=_("Community")
    )
    text = models.TextField(
        verbose_name=_("Text")
    )
    source = models.CharField(
        max_length=50,
        verbose_name=_("Source")
    )  # where the post is from
    views = models.IntegerField(
        default=0,
        verbose_name="Views"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date")
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class CommunityManager(models.Model):
    """
    A manager of a community with their status, contact link, and avatar
    """
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name=_("Community")
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    status = models.CharField(
        max_length=10,
        verbose_name=_("Status")

    )
    contact_link = models.URLField(
        verbose_name=_("Contact link")
    )
    avatar = models.ImageField(
        upload_to='images\\manager_avatars',
        verbose_name=_("Avatar")
    )

    class Meta:
        verbose_name = _("Community manager")
        verbose_name_plural = _("Community managers")


class SocialLink(models.Model):
    """
    A social media link associated with a community
    """
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        verbose_name=_("Community")
    )
    platform = models.CharField(
        max_length=20,
        verbose_name=_("Social Platform")
    )
    link = models.URLField(
        verbose_name=_("Social link")
    )

    class Meta:
        verbose_name = _("Social media link")
        verbose_name_plural = _("Social media links")


class LatestPostView(models.Model):
    """
    A view of a post, tracked over time
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        verbose_name=_("Post")
    )
    views = models.IntegerField(
        default=0,
        verbose_name=_("Count of views")
    )
    recording_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date of recording")
    )

    class Meta:
        verbose_name = _("Latest post views record")
        verbose_name_plural = _("Latest post views records")
