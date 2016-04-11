# coding=utf-8
from django.db import models
from apps.city.models import City
from core.models import User

__author__ = 'alexy'


class Moderator(models.Model):
    class Meta:
        verbose_name = u'Модератор'
        verbose_name_plural = u'Модераторы'
        app_label = 'moderator'

    def __unicode__(self):
        if self.company:
            return self.company
        else:
            return self.user.get_full_name()

    user = models.OneToOneField(
        to=User,
        limit_choices_to={'type': 2},
        verbose_name=u'Модератор',
        related_name='moderator_user'
    )
    city = models.ManyToManyField(
        to=City,
        verbose_name=u'Город',
        blank=True,
        null=True
    )
    company = models.CharField(
        verbose_name=u'Название организации',
        max_length=200,
    )
    leader = models.CharField(
        verbose_name=u'Руководитель',
        max_length=200,
        blank=True,
        null=True
    )
    leader_function = models.CharField(
        verbose_name=u'Должность руководителя',
        max_length=200,
        blank=True,
        null=True
    )
    work_basis = models.CharField(
        verbose_name=u'Должность руководителя',
        max_length=200,
        blank=True,
        null=True
    )


class ModeratorArea(models.Model):
    class Meta:
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'
        app_label = 'moderator'

    def __unicode__(self):
        return self.name

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    name = models.CharField(max_length=100, verbose_name=u'Название')
