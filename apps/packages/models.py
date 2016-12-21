# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models

__author__ = 'alexy'


class Package(models.Model):
    class Meta:
        verbose_name = u'Пакет подписки'
        verbose_name_plural = u'Пакеты подписок'
        app_label = 'packages'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('package:update', args=(self.id, ))

    MONTH_CHOICE = (
        (1, u'1 месяц'),
        (2, u'2 месяца'),
        (3, u'3 месяца'),
        (4, u'4 месяца'),
        (5, u'5 месяцев'),
        (6, u'6 месяцев'),
        (7, u'7 месяцев'),
        (8, u'8 месяцев'),
        (9, u'9 месяцев'),
        (10, u'10 месяцев'),
        (11, u'11 месяцев'),
        (12, u'12 месяцев')
    )

    name = models.CharField(verbose_name=u'Название', max_length=255)
    discount = models.CharField(verbose_name=u'Скидка', max_length=255, blank=True, null=True)
    month = models.PositiveIntegerField(default=1, choices=MONTH_CHOICE, verbose_name=u'Количество месяцев')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Стоимость, руб')
