# coding=utf-8
from django.db import models
from apps.moderator.models import Moderator
from core.models import User

__author__ = 'alexy'


class Distributor(models.Model):
    class Meta:
        verbose_name = u'Распространитель'
        verbose_name_plural = u'Распространители'
        app_label = 'distributor'

    def __unicode__(self):
        return self.user.get_full_name()

    user = models.OneToOneField(
        to=User,
        limit_choices_to={'type': 4},
        verbose_name=u'Пользователь',
        related_name='distributor_user'
    )
    moderator = models.ForeignKey(
        to=Moderator,
        verbose_name=u'Модератор'
    )
