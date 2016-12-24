# coding=utf-8
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from apps.correspondence.models import UserMessage, UserMessageAnswer

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        message_qs = UserMessage.objects.filter(is_send=False)
        answer_qs = UserMessageAnswer.objects.filter(is_send=False)
        message_subject = u'Новое сообщение в кабинете reklamadoma.com'
        answer_subject = u'Ответ на ваше сообщение в кабинете reklamadoma.com'
        url = reverse('correspondence:usermessage-list')
        message = u'Для просмотра сообщений перейдите по ссылке: http://reklamadoma.com%s' % url
        message_recipient_list = [i.recipient.email for i in message_qs]
        answer_recipient_list = [i.recipient.email for i in answer_qs]
        try:
            if message_recipient_list:
                send_mail(
                    message_subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    message_recipient_list
                )
                message_qs.update(is_send=True)
        except:
            pass
        try:
            if answer_recipient_list:
                send_mail(
                    answer_subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    answer_recipient_list
                )
                answer_qs.update(is_send=True)
        except:
            pass
