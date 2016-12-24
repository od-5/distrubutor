# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from apps.moderator.models import Moderator
from core.base_model import Common
from core.models import User

__author__ = 'alexy'


class CommonMessage(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created', ]

    author = models.ForeignKey(to=User, verbose_name=u'Автор')
    created = models.DateTimeField(verbose_name=u'Дата создания', auto_now=True)


class CommonNotify(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created', ]

    is_view = models.BooleanField(default=False, verbose_name=u'Просмотрено')
    is_send = models.BooleanField(default=False, verbose_name=u'Оповещение отправлено')


class Message(CommonMessage):
    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'
        app_label = 'correspondence'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('correspondence:detail', args=(self.pk,))

    title = models.CharField(max_length=100, verbose_name=u'Тема')
    text = models.TextField(verbose_name=u'Текст сообщения')


class UserMessage(CommonNotify):
    class Meta:
        verbose_name = u'Сообщение для пользователя'
        verbose_name_plural = u'Сообщения для пользователей'
        app_label = 'correspondence'
        ordering = ['-message__created']

    def __unicode__(self):
        return self.message.title

    def get_absolute_url(self):
        return reverse('correspondence:usermessage-detail', args=(self.pk,))

    message = models.ForeignKey(to=Message, verbose_name=u'Сообщение')
    recipient = models.ForeignKey(to=User, verbose_name=u'Получатель')


class UserMessageAnswer(CommonMessage, CommonNotify):
    class Meta:
        verbose_name = u'Ответ на сообщение'
        verbose_name_plural = u'Ответы на сообщения'
        app_label = 'correspondence'

    usermessage = models.ForeignKey(to=UserMessage, verbose_name=u'Сообщение пользователя')
    text = models.TextField(verbose_name=u'Текст сообщения')
    recipient = models.ForeignKey(to=User, verbose_name=u'Получатель', related_name='usermessageanswer_recipient')