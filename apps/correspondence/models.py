# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from apps.moderator.models import Moderator
from core.base_model import Common
from core.models import User

__author__ = 'alexy'


class Message(models.Model):
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
    author = models.ForeignKey(to=User, verbose_name=u'Автор')
    created = models.DateTimeField(verbose_name=u'Дата создания', auto_now=True)


class MessageNotify(models.Model):
    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'
        app_label = 'correspondence'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('correspondence:message-detail', args=(self.pk,))

    message = models.ForeignKey(to=Message, verbose_name=u'Сообщение')
    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Получатель')
    is_view = models.BooleanField(default=False, verbose_name=u'Просмотрено')