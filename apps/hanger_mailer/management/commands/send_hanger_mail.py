# coding=utf-8
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.hanger_mailer.models import HangerMailItem

__author__ = 'alexy'


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = HangerMailItem.objects.all()
        message = u'Это письмо отправлено автоматически через сервис reklamadoma.com. \
         Для обратной связи воспользуйтесь контактными данными из тела письма'
        for mail in qs:

            msg_html = render_to_string(
                'hanger_mailer/mail.html',
                {'phone': mail.hangermail.phone, 'price': mail.hangermail.price, 'count': mail.hangermail.count}
            )
            try:
                send_mail(
                    mail.hangermail.title,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [mail.email, ],
                    html_message=msg_html,
                )
            except:
                pass
            hanger_mailer = mail.hangermail
            hanger_mailer.mail_count += 1
            hanger_mailer.save()
            mail.delete()
