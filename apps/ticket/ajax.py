# coding=utf-8
from annoying.decorators import ajax_request
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def hanger_ticket(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    mail = request.POST.get('mail')
    theme = request.POST.get('theme')
    site = request.POST.get('site')
    success = False
    if site and site == 'hanger-reklama.com':
        if name and phone and mail and theme:
            success = True
    return {
        'success': success
    }
