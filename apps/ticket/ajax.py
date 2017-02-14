# coding=utf-8
from annoying.decorators import ajax_request
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from apps.geolocation.models import City

__author__ = 'alexy'

import logging
logger = logging.getLogger('django.request')


@ajax_request
@csrf_exempt
def hanger_ticket(request):
    name = request.POST.get('name') or ''
    phone = request.POST.get('phone') or ''
    mail = request.POST.get('mail') or ''
    theme = request.POST.get('theme') or ''
    city_name = request.POST.get('city') or ''
    logger.error(u'name: %s, phone: %s, mail: %s, theme: %s, city_name: %s' % (name, phone, mail, theme, city_name))
    if city_name:
        city = City.objects.filter(name=city_name).first()
        if city:
            moderator = city.moderator_set.filter(stand_accept=True).first()
            if moderator:
                return {
                    'success': True,
                    'name': name,
                    'phone': phone,
                    'mail': mail,
                    'theme': theme,
                    'city': city.name,
                    'moderator': moderator.__unicode__()
                }
            else:
                return {
                    'success': False,
                    'message': u'Not moderator found'
                }
        else:
            return {
                'success': False,
                'message': u'Not city found'
            }
    return {
        'success': False,
    }
