# coding=utf-8
import factory

from core.tests.fixtures import UserFactory
from ..models import Section, Topic, Comment, Notification


class ForumCommonFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)


class SectionFactory(ForumCommonFactory):
    class Meta:
        model = Section

    title = u'Раздел форума'


class TopicFactory(ForumCommonFactory):
    class Meta:
        model = Topic

    section = factory.SubFactory(SectionFactory)
    title = u'Тема форума'
    text = u'Сообщение'


class CommentFactory(ForumCommonFactory):
    class Meta:
        model = Comment

    topic = factory.SubFactory(TopicFactory)
    text = u'Комментарий'


class NotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Notification

    topic = factory.SubFactory(TopicFactory)
