import datetime
from .models import Setup

__author__ = 'alexy'


def paginator_link(request):
    get_data = request.GET.copy()
    filtered_url = '?'
    for i in get_data:
        if i != 'page':
            filtered_url += u'%s=%s&' % (i, get_data[i])
    return {
        'URL_WITH_FILTER': filtered_url
    }


def site_setup(request):
    if not request.subdomain:
        main_page = True
    else:
        main_page = False
    return {
        'CURRENT_YEAR': datetime.datetime.now(),
        'MAIN_PAGE': main_page,
    }
