# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q

from core.models import User

__author__ = 'alexy'


class ManagerModelManager(models.Manager):
    def get_qs(self, user):
        qs = Manager.objects.none()

        if user.type == User.UserType.administrator:
            qs = Manager.objects.all()
        elif user.type == User.UserType.moderator:
            if user.superviser:
                qs = Manager.objects.filter(
                    Q(moderator__moderator_user__superviser=user) | Q(moderator=user))
            else:
                qs = Manager.objects.filter(moderator=user)
        elif user.type == User.UserType.manager:
            manager = Manager.objects.get(user=user)
            qs = Manager.objects.filter(moderator=manager.moderator)

        return qs


class Manager(models.Model):
    class Meta:
        verbose_name = u'Менеджер'
        verbose_name_plural = u'Менеджеры'
        app_label = 'manager'

    def __unicode__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('manager:update', args=(self.pk, ))

    objects = ManagerModelManager()

    user = models.OneToOneField(to=User, verbose_name=u'Пользователь', related_name='manager_user')
    moderator = models.ForeignKey(
        to=User, verbose_name=u'Модератор', limit_choices_to={'type': User.UserType.moderator})
    leader = models.BooleanField(verbose_name=u'Руководитель группы', default=False)
