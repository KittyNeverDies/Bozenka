from django.shortcuts import render


def page_not_found_view(request, exception):
    """
    View for page not found.
    :param request: Your request
    :param exception: Exception
    :return:
    """
    return render(request, 'error/404.html', status=404)