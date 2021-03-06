# coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField

from apps.geolocation.models import City
from core.models import User

__author__ = 'alexy'


class ForumCommon(models.Model):
    author = models.ForeignKey(to=User, verbose_name=u'Автор')
    created = models.DateTimeField(verbose_name=u'Дата создания', auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']


class ForumBase(ForumCommon):
    city = models.ManyToManyField(to=City, blank=True, null=True, verbose_name=u'Города')
    moderator = models.BooleanField(verbose_name=u'Модератор', default=True)
    leader = models.BooleanField(verbose_name=u'Руководитель группы', default=True)
    manager = models.BooleanField(verbose_name=u'Менеджер', default=True)
    distributor = models.BooleanField(verbose_name=u'Распространитель', default=True)

    class Meta:
        abstract = True


class Section(ForumBase):
    title = models.CharField(max_length=256, verbose_name=u'Название')
    description = models.TextField(verbose_name=u'Краткое описание', blank=True, null=True)

    class Meta:
        verbose_name = u'Раздел форумы'
        verbose_name_plural = u'Разделы форума'
        app_label = 'forum'

    def __unicode__(self):
        return self.title

    def topic_count(self):
        return self.topic_set.count()

    def comment_count(self):
        return Comment.objects.select_related().filter(topic__section=self).count()

    def get_last_comment(self):
        return Comment.objects.select_related().filter(topic__section=self).last()


class Topic(ForumBase):
    section = models.ForeignKey(to=Section, verbose_name=u'Раздел')
    title = models.CharField(max_length=256, verbose_name=u'Название')
    text = RichTextField(verbose_name=u'Сообщение')
    all_city = models.BooleanField(verbose_name=u'Доступно всем городам', default=False)
    closed = models.BooleanField(verbose_name=u'Тема закрыта', default=False)

    class Meta:
        verbose_name = u'Тема'
        verbose_name_plural = u'Темы'
        app_label = 'forum'

    def __unicode__(self):
        return self.title

    def get_city_id_list(self):
        return [int(city.id) for city in self.city.all()]

    def notification_recipients(self):
        if self.moderator:
            moderator_qs = User.objects.filter(type=User.UserType.moderator, is_active=True)
            if moderator_qs and not self.all_city:
                moderator_qs = moderator_qs.filter(moderator_user__city__in=self.get_city_id_list()).distinct()
            for user in moderator_qs:
                notification = Notification(topic=self, user=user)
                notification.save()
        if self.leader:
            leader_qs = User.objects.select_related().filter(
                type=User.UserType.manager, manager_user__leader=True, is_active=True)
            if leader_qs and not self.all_city:
                leader_qs = leader_qs.filter(
                    manager_user__moderator__moderator_user__city__in=self.get_city_id_list()).distinct()
            for user in leader_qs:
                notification = Notification(topic=self, user=user)
                notification.save()
        if self.manager:
            manager_qs = User.objects.select_related().filter(
                type=User.UserType.manager, manager_user__leader=False, is_active=True)
            if manager_qs and not self.all_city:
                manager_qs = manager_qs.filter(
                    manager_user__moderator__moderator_user__city__in=self.get_city_id_list()).distinct()
            for user in manager_qs:
                notification = Notification(topic=self, user=user)
                notification.save()
        if self.distributor:
            distributor_qs = User.objects.select_related().filter(type=User.UserType.distributor, is_active=True)
            if distributor_qs and not self.all_city:
                distributor_qs = distributor_qs.filter(
                    distributor_user__moderator__city__in=self.get_city_id_list()).distinct()
            for user in distributor_qs:
                notification = Notification(topic=self, user=user)
                notification.save()
        return None

    def get_last_comment(self):
        return self.comment_set.last()

    def get_absolute_url(self):
        return reverse('forum:topic-detail', args=(self.pk, ))

    def get_comment_count(self):
        return self.comment_set.count()


class Comment(ForumCommon):
    class Meta:
        verbose_name = u'Сообщение'
        verbose_name_plural = u'Сообщения'
        app_label = 'forum'

    def __unicode__(self):
        return self.author.get_full_name()

    def get_comment_link(self):
        topic_link = reverse('forum:topic-detail', args=(self.topic.id, ))
        return '%s#%s' % (topic_link, self.id)

    topic = models.ForeignKey(to=Topic, verbose_name=u'Тема')
    text = RichTextField(verbose_name=u'Сообщение')


class Notification(models.Model):
    """
    notification class
    """
    topic = models.ForeignKey(to=Topic)
    user = models.ForeignKey(to=User)
