# coding=utf-8
from django.db import models
from apps.city.models import City
from apps.moderator.models import Moderator
from core.base_model import Common
from core.models import User

__author__ = 'alexy'


class Ticket(Common):
    class Meta:
        verbose_name = u'Заявка'
        verbose_name_plural = u'Заявки'
        app_label = 'ticket'

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
    name = models.CharField(verbose_name=u'Имя', max_length=256)
    mail = models.EmailField(verbose_name=u'E-mail', max_length=20, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=20, blank=True, null=True)
    type = models.PositiveSmallIntegerField(verbose_name=u'Статус заявки', choices=TICKET_TYPE_CHOICE,
                                            default=1, blank=True, null=True)
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name=u'Сумма')
