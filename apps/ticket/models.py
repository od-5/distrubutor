# coding=utf-8
from django.db import models
from apps.geolocation.models import City
from apps.moderator.models import Moderator
from core.base_model import Common
from core.models import User

__author__ = 'alexy'


class Ticket(Common):
    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        app_label = 'ticket'
        ordering = ['-created']

    def __unicode__(self):
        return u'Заявка на имя: %s, телефон: %s' % (self.name, self.phone)

    def performed_at(self):
        pass

    TICKET_TYPE_CHOICE = (
        (0, u'Новая заявка'),
        (1, u'В обработке'),
        (2, u'Отклонена'),
        (3, u'Продажа'),
    )

    city = models.ForeignKey(to=City, verbose_name=u'Город', blank=True, null=True)
    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Исполнитель', blank=True, null=True)
    agency_manager = models.ForeignKey(to=User, limit_choices_to={'type': 6},
                                       verbose_name=u'Менеджер РА', blank=True, null=True)
    name = models.CharField(verbose_name=u'Имя', max_length=256, blank=True, null=True)
    mail = models.EmailField(verbose_name=u'E-mail', max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=20, blank=True, null=True)
    type = models.PositiveSmallIntegerField(verbose_name=u'Статус заявки', choices=TICKET_TYPE_CHOICE,
                                            default=1, blank=True, null=True)
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name=u'Сумма')
    hanger = models.BooleanField(default=False, verbose_name=u'Заявка с сайта hanger-reklama.com')


class PreSale(Common):
    class Meta:
        verbose_name = u'Преданный клиент'
        verbose_name_plural = u'Переданные клиенты'
        app_label = 'ticket'

    def __unicode__(self):
        return self.legal_name

    ticket = models.OneToOneField(to=Ticket, verbose_name=u'Заявка')
    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Исполнитель')
    legal_name = models.CharField(verbose_name=u'Название организации', max_length=256)
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    accept = models.BooleanField(default=False, verbose_name=u'Принят в работу')
    commission = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Комиссия с продаж, %')
