# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum

from apps.manager.models import Manager
from apps.moderator.models import Moderator

__author__ = 'alexy'


class Stand(models.Model):
    class Meta:
        verbose_name = u'Вёрстка'
        verbose_name_plural = u'Вёрстки'
        app_label = 'stand'
        ordering = ['-date_start', ]

    def __unicode__(self):
        if self.name:
            return u'%s %s - %s ' % (self.name, self.date_start, self.date_end)
        else:
            return u'Стенд %s - %s ' % (self.date_start, self.date_end)

    def get_total_sum(self):
        total_sum = self.standitem_set.aggregate(Sum('sum'))['sum__sum']
        return total_sum

    def get_absolute_url(self):
        return reverse('stand:update', args=(self.pk, ))

    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    name = models.CharField(max_length=256, verbose_name=u'Название', blank=True, null=True)
    date_start = models.DateField(verbose_name=u'Дата начала')
    date_end = models.DateField(verbose_name=u'Дата окончания')


class StandItem(models.Model):
    class Meta:
        verbose_name = u'Элемент вёрстки'
        verbose_name_plural = u'Элементы вёрстки'
        app_label = 'stand'
        ordering = ['-created', ]

    SIDE_CHOICES = (
        ('front', u'Сторона А'),
        ('back', u'Сторона Б'),
    )

    POSITION_CHOICES = (
        ('top', u'Верх'),
        ('bottom', u'Низ'),
    )

    stand = models.ForeignKey(to=Stand, verbose_name=u'Вёрстка')
    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер', blank=True, null=True)
    moderator = models.BooleanField(verbose_name=u'Модератор', default=False)
    client = models.TextField(verbose_name=u'Название клиента', blank=True, null=True)
    side = models.CharField(max_length=5, verbose_name=u'Сторона', choices=SIDE_CHOICES)
    position = models.CharField(max_length=6, verbose_name=u'Сторона', choices=POSITION_CHOICES)
    width = models.PositiveIntegerField(verbose_name=u'Ширина', default=0)
    height = models.PositiveIntegerField(verbose_name=u'Высота', default=0)
    top = models.PositiveIntegerField(verbose_name=u'Отступ сверху', default=0)
    left = models.PositiveIntegerField(verbose_name=u'Отступ слева', default=0)
    sum = models.DecimalField(verbose_name=u'Сумма', blank=True, null=True, max_digits=10, decimal_places=2)
    created = models.DateField(verbose_name=u'Дата создания')
