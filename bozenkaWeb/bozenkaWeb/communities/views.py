from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.db.models import Q
from .models import Community, Tag


def index(request: WSGIRequest):
    """
    Main view of the list of communities.
    :param request: Request object
    :return: Returns HTTP response.
    """

    # List of communities & tags
    communities_list = Community.objects.all()
    tags = Tag.objects.all()

    # Handle search request
    query = request.GET.get('q')
    selected_tags = request.GET.getlist('tags')

    if query:
        communities_list = communities_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(short_description__icontains=query)
        )

    if selected_tags:
        communities_list = communities_list.filter(tags__name__in=selected_tags).distinct()
    return render(
        request,
        "communities/list.html",
        {
            "communities_list": communities_list,
            "tags": tags,
            "selected_tags": selected_tags,
            "query": query
        }
    )
