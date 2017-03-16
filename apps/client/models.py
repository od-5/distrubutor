# coding=utf-8
from django.core.urlresolvers import reverse
from django.db import models
from apps.geolocation.models import City
from apps.manager.models import Manager
from apps.moderator.models import Moderator

__author__ = 'alexy'


class ClientModelManager(models.Manager):

    def get_qs(self, user):
        if user.type == 1:
            qs = Client.objects.all()
        elif user.type == 2:
            qs = Client.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = Client.objects.filter(moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = Client.objects.filter(manager=user.manager_user)
        else:
            qs = Client.objects.none()
        return qs


class Client(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'client'

    def __unicode__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('client:update', args=(self.pk, ))

    TYPE_CHOICES = (
        (0, u'Входящая заявка'),
        (1, u'Клиент'),
        (2, u'Переданный клиент'),
    )

    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер')
    name = models.CharField(verbose_name=u'Название', max_length=255)
    city = models.ForeignKey(to=City, verbose_name=u'Город')
    kind_of_activity = models.CharField(verbose_name=u'Вид деятельности', max_length=255, blank=True, null=True)
    actual_address = models.CharField(verbose_name=u'Фактический адрес', max_length=255, blank=True, null=True)
    site = models.CharField(verbose_name=u'Сайт', blank=True, null=True,  max_length=100)
    type = models.PositiveSmallIntegerField(verbose_name=u'Тип клиента', choices=TYPE_CHOICES, default=TYPE_CHOICES[1][0])

    objects = ClientModelManager()


class ClientManager(models.Model):
    class Meta:
        verbose_name = u'менеджер клиента'
        verbose_name_plural = u'менеджеры клиента'
        app_label = 'client'

    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер')
    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    date = models.DateField(auto_now_add=True, verbose_name=u'Дата назначения')


class ClientContact(models.Model):
    class Meta:
        verbose_name = u'Контактное лицо'
        verbose_name_plural = u'Контактные лица'
        app_label = 'client'

    def __unicode__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('client:contact-update', args=(self.pk, ))

    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    name = models.CharField(verbose_name=u'ФИО', max_length=255)
    function = models.CharField(verbose_name=u'Должность', max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=30, blank=True, null=True)
    email = models.EmailField(verbose_name=u'e-mail', max_length=50, blank=True, null=True)


class Task(models.Model):
    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'
        app_label = 'client'
        ordering = ['-date', ]

    def __unicode__(self):
        return self.get_type_display()

    # def get_absolute_url(self):
    #     return reverse('client:task-update', args=(self.pk, ))

    TASK_TYPE_CHOICES = (
        (0, u'Назначена встреча'),
        (1, u'Назначен звонок'),
        (2, u'Продажа'),
        (3, u'Отказ'),
    )

    TASK_STATUS = (
        (0, u'План'),
        (1, u'Сделано'),
    )

    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер')
    client = models.ForeignKey(to=Client, verbose_name=u'Клиент')
    clientcontact = models.ForeignKey(to=ClientContact, verbose_name=u'Контактное лицо', null=True, blank=True)
    type = models.PositiveIntegerField(choices=TASK_TYPE_CHOICES, verbose_name=u'Тип задачи')
    date = models.DateField(verbose_name=u'Дата')
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    status = models.PositiveIntegerField(choices=TASK_STATUS, default=0, verbose_name=u'Статус')
