# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from apps.geolocation.models import City

from apps.manager.models import Manager
from apps.moderator.models import Moderator
from core.base_model import Common

__author__ = 'alexy'


class HangerMail(Common):
    class Meta:
        verbose_name = u'Рассылка'
        verbose_name_plural = u'Рассылка'
        app_label = 'hanger_mailer'
        ordering = ['-created', ]

    def __unicode__(self):
        return u'Рассылка город %s - %s' % (self.city.name, self.title)

    def get_absolute_url(self):
        return reverse('hanger_mailer:update', args=(self.pk, ))

    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    title = models.CharField(max_length=256, verbose_name=u'Тема')
    phone = models.CharField(max_length=100, verbose_name=u'Телефон', blank=True, null=True)
    count = models.PositiveIntegerField(verbose_name=u'Количество экземпляров', blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name=u'Стоимость, руб', blank=True, null=True)


class HangerMailItem(models.Model):
    class Meta:
        verbose_name = u'Письмо'
        verbose_name_plural = u'Письма'
        app_label = 'hanger_mailer'

    hangermail = models.ForeignKey(to=HangerMail)
    email = models.EmailField(max_length=60, verbose_name=u'email')