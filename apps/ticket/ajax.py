# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from apps.city.models import City
from apps.moderator.models import Moderator
from core.models import Setup
from .forms import TicketAddForm

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def ticket(request):
    email = None
    try:
        email = Setup.objects.all()[0].email
    except:
        email = 'od-5@yandex.ru'
    if request.method == "POST":
        form = TicketAddForm(data=request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.type = 0
            ticket.save()
            theme = request.POST.get('theme')
            mail_title_msg = u'Новая заявка на сайте reklamadoma.com'
            message = u'Имя: %s\nТелефон: %s\n' % (ticket.name, ticket.phone)
            if email:
                send_mail(
                    mail_title_msg,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ]
                )
            return {
                'success': u'Ваша заявка принята. Наши менеджеры свяжуться с вами в ближайшее в время!'
            }
        else:
            return {
                'error': u'Пожалуйста заполните все поля в форме!'
            }
    else:
        return {
            'error': u'Упс. Заявки то можно отправлять только непсредственно с сайта!'
        }
