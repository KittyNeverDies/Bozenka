from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render


def home_page(request: WSGIRequest):
    """
    View, that was made for only returning home page :P
    :param request: WSGIRequest object
    :return: Rendered page
    """
    return render(request, "homepage\\index.html")

