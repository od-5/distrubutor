# coding=utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.geolocation.tests.fixtures import CityFactory
from apps.moderator.tests.fixtures import ModeratorFactory
from apps.manager.tests.fixtures import ManagerFactory
from apps.distributor.tests.fixtures import DistributorFactory
from .fixtures import SectionFactory, TopicFactory, CommentFactory
from ..models import Topic, Comment, Notification


class SectionTestCase(TestCase):

    def setUp(self):
        self.section = SectionFactory()

    def test_string_representation(self):
        self.assertEqual(unicode(self.section), self.section.title)

    def test_topic_count(self):
        self.assertEqual(Topic.objects.filter(section=self.section).count(), self.section.topic_count())
        TopicFactory(section=self.section)
        self.assertEqual(Topic.objects.filter(section=self.section).count(), self.section.topic_count())

    def test_comment_count(self):
        topic = TopicFactory(section=self.section)
        other_topic = TopicFactory(section=self.section)
        CommentFactory(topic=topic)
        CommentFactory(topic=other_topic)
        CommentFactory()

        self.assertEqual(Comment.objects.filter(topic__section=self.section).count(), self.section.comment_count())

    def test_get_last_comment(self):
        CommentFactory(topic__section=self.section)
        last_comment = CommentFactory(topic__section=self.section)
        CommentFactory()

        self.assertEqual(last_comment.pk, self.section.get_last_comment().pk)


class TopicTestCase(TestCase):

    def setUp(self):
        self.topic = TopicFactory(moderator=False, manager=False, leader=False, distributor=False)

    def test_string_representation(self):
        self.assertEqual(unicode(self.topic), self.topic.title)

    def test_city_id_list(self):
        self.topic.city.add(CityFactory())
        self.assertListEqual(list(self.topic.city.values_list('id', flat=True)), self.topic.get_city_id_list())

    def test_notification_recipients_moderator(self):
        city = CityFactory()
        self.topic.moderator = True
        self.topic.city.add(city)
        ModeratorFactory(city=(city,))
        ModeratorFactory()

        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 1)
        Notification.objects.all().delete()

        self.topic.all_city = True
        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 2)

    def test_notification_recipients_leader(self):
        city = CityFactory()
        self.topic.leader = True
        self.topic.city.add(city)
        ManagerFactory(leader=True).moderator.moderator_user.city.add(city)
        ManagerFactory(leader=True)

        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 1)
        Notification.objects.all().delete()

        self.topic.all_city = True
        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 2)

    def test_notification_recipients_manager(self):
        city = CityFactory()
        self.topic.manager = True
        self.topic.city.add(city)
        ManagerFactory(leader=False).moderator.moderator_user.city.add(city)
        ManagerFactory(leader=False)

        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 1)
        Notification.objects.all().delete()

        self.topic.all_city = True
        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 2)

    def test_notification_recipients_distributor(self):
        city = CityFactory()
        self.topic.distributor = True
        self.topic.city.add(city)
        DistributorFactory().moderator.city.add(city)
        DistributorFactory()

        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 1)
        Notification.objects.all().delete()

        self.topic.all_city = True
        self.topic.notification_recipients()
        self.assertEqual(Notification.objects.count(), 2)

    def test_get_last_comment(self):
        CommentFactory(topic=self.topic)
        last_comment = CommentFactory(topic=self.topic)
        CommentFactory()
        CommentFactory(topic__section=self.topic.section)

        self.assertEqual(last_comment.pk, self.topic.get_last_comment().pk)

    def test_get_absolute_url(self):
        self.assertEqual(reverse('forum:topic-detail', args=(self.topic.pk, )), self.topic.get_absolute_url())

    def test_get_comment_count(self):
        CommentFactory(topic=self.topic)
        CommentFactory()
        CommentFactory(topic__section=self.topic.section)

        self.assertEqual(Comment.objects.filter(topic=self.topic).count(), self.topic.get_comment_count())


class CommentTestCase(TestCase):

    def setUp(self):
        self.comment = CommentFactory()

    def test_string_representation(self):
        self.assertEqual(unicode(self.comment), self.comment.author.get_full_name())

    def test_get_comment_link(self):
        self.assertEqual('%s#%s' % (reverse('forum:topic-detail', args=(self.comment.topic.id, )), self.comment.id),
                         self.comment.get_comment_link())
