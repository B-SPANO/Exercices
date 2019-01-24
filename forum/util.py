from django.core.paginator import Paginator, EmptyPage, InvalidPage
from forum import settings as forum_settings

# def absolute_url(path):
#     return 'http://%s%s' % (Site.objects.get_current().domain, path)


def get_page(objects, request, size):
    try:
        return Paginator(objects, size).page(request.GET.get('page', 1))
    except InvalidPage:
        return None


def build_form(Form, _request, GET=False, *args, **kwargs):
    """
    Shorcut for building the form instance of given form class
    """

    if not GET and 'POST' == _request.method:
        form = Form(_request.POST, _request.FILES, *args, **kwargs)
    elif GET and 'GET' == _request.method:
        form = Form(_request.GET, _request.FILES, *args, **kwargs)
    else:
        form = Form(*args, **kwargs)
    return form