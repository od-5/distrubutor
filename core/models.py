# coding=utf-8
import os
from random import randint
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import SmartResize
from core.files import upload_to

__author__ = 'alexy'


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            password = User.objects.make_random_password()

        kwargs.update({'email': self.normalize_email(email)})
        user = self.model(**kwargs)
        user.set_password(password)
        user.original_password = password
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name=None, last_name=None, patronymic=None):
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def normalize_email(self, email):
        email = super(MyUserManager, self).normalize_email(email)
        return email.lower()


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
        ordering = ['-date_joined']
        app_label = 'core'

    USER_TYPE_CHOICE = (
        (1, u'Администратор'),
        (2, u'Модератор'),
        (3, u'Клиент'),
        (4, u'Распространитель'),
        (5, u'Менеджер'),
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True, default=u'')
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True, default=u'')
    patronymic = models.CharField(u'Отчество', max_length=50, blank=True, null=True, default=u'')
    phone = models.CharField(max_length=250, verbose_name=u'Телефон', null=True, blank=True, default=u'')
    type = models.PositiveSmallIntegerField(verbose_name=u'Уровень доступа', default=1, choices=USER_TYPE_CHOICE)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    # def get_absolute_url(self):
    #     if self.type == 1:
    #         return reverse('administrator:change', args=(self.pk, ))
    #     if self.type == 2:
    #         return reverse('moderator:change', args=(self.pk, ))
    #     else:
    #         return reverse('cabinet:cabinet')
    #
    # def get_change_url(self):
    #     return reverse('cabinet:user-change', args=(self.pk, ))
    def is_leader_manager(self):
        if self.type == 1 or self.type == 2:
            return True
        if self.type == 5:
            if self.manager_user.leader:
                return True
        return False

    def deny_access(self):
        if self.type == 1 or self.type == 3:
            return False
        elif self.type == 2:
            if self.moderator_user.deny_access or not self.moderator_user:
                return True
            else:
                return False
        elif self.type == 4 and self.distributor_user.moderator.deny_access:
            return True
        elif self.type == 5 and self.manager_user.moderator.moderator_user.deny_access:
            return True
        else:
            return False

    def get_full_name(self):
        return u'%s %s %s' % (self.last_name, self.first_name or '', self.patronymic or '')

    def get_short_name(self):
        return u'%s' % self.first_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Setup(models.Model):
    class Meta:
        verbose_name = u'Настройки сайта'
        verbose_name_plural = u'Настройки сайта'
        app_label = 'core'
        ordering = ('id', )

    def __unicode__(self):
        return u'Настройки сайта'

    meta_title = models.CharField(verbose_name=u'Заголовок сайта', max_length=256)
    meta_keys = models.TextField(verbose_name=u'Ключевые слова', blank=True, null=True)
    meta_desc = models.TextField(verbose_name=u'Мета описание', blank=True, null=True)
    email = models.EmailField(verbose_name=u'e-mail для приёма заявок')
    video = models.TextField(verbose_name=u'HTML-код видео', blank=True, null=True)
    top_js = models.TextField(verbose_name=u'Скрипты в <HEAD>..</HEAD>', blank=True)
    bottom_js = models.TextField(verbose_name=u'Скрипты перед закрывающим </BODY>', blank=True)
    robots_txt = models.TextField(verbose_name=u'robots.txt', blank=True, null=True)
