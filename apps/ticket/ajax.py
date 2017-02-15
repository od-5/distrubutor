# coding=utf-8
import urllib
import logging

from annoying.decorators import ajax_request
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from apps.geolocation.models import City
from apps.ticket.models import Ticket

__author__ = 'alexy'


logger = logging.getLogger('django.request')


@ajax_request
@csrf_exempt
def hanger_ticket(request):
    name = request.POST.get('name') or ''
    phone = request.POST.get('phone') or ''
    mail = request.POST.get('mail') or ''
    theme = request.POST.get('theme') or ''
    city_name = request.POST.get('city') or ''
    logger.error(u'name: %s, phone: %s, mail: %s, theme: %s, city_name: %s' %
                 (name, phone, mail, theme, urllib.unquote(city_name)))
    if city_name:
        city = City.objects.filter(name=urllib.unquote(city_name)).first()
        if city:
            moderator = city.moderator_set.filter(stand_accept=True).first()
            if moderator:
                ticket = Ticket(city=city, moderator=moderator, hanger=True)
                if name:
                    ticket.name = name
                if phone:
                    ticket.phone = phone
                if mail:
                    ticket.mail = mail
                ticket.save()
                try:
                    theme = u'Заявка с сайта hanger-reklama.com'
                    mail_title_msg = u'Новая заявка на сайте reklamadoma.com'
                    message = u'Тема: %s\nИмя: %s\nТелефон: %s\n' % (theme, ticket.name, ticket.phone)
                    send_mail(
                        mail_title_msg,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [ticket.moderator.user.email, ]
                    )
                except:
                    pass
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
