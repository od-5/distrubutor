# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from apps.city.models import City
from apps.moderator.models import Moderator
from core.models import Setup
from .forms import TicketAddForm

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def ticket(request):
    """
    Сохранение заявки с сайте в базе.
    Отправка письма с уведомлением о новой заявке модератору или рекламному агенству.
    todo: отправка шаблонного письма на email указанный в заявке
    """
    try:
        email = Setup.objects.all()[0].email
    except:
        email = 'od-5@yandex.ru'
    if request.method == "POST":
        form = TicketAddForm(data=request.POST)
        if request.POST.get('moderator'):
            moderator = Moderator.objects.get(pk=int(request.POST.get('moderator')))
            if not moderator.ticket_forward:
                email = Moderator.objects.select_related().get(pk=int(request.POST.get('moderator'))).user.email
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.type = 0
            ticket.save()
            theme = request.POST.get('theme')
            mail_title_msg = u'Новая заявка на сайте reklamadoma.com'
            message = u'Тема: %s\nИмя: %s\nТелефон: %s\n' % (theme, ticket.name, ticket.phone)
            if email:
                send_mail(
                    mail_title_msg,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ]
                )
            # todo: if ticket.mail - отправить на эту почту шаблонное письмо
            if ticket.mail:
                subject = u'Спасибо за заявку на сайте reklamadoma.com'
                # msg_plain = render_to_string('email.txt', {'name': name})
                msg_html = render_to_string('ticket/mail.html')
                try:
                    send_mail(
                        subject,
                        msg_html,
                        settings.DEFAULT_FROM_EMAIL,
                        [ticket.mail, ],
                        html_message=msg_html,
                    )
                except:
                    pass


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
