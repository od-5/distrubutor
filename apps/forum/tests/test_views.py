# coding=utf-8
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from core.tests.base import LoginWithUserTestCase
from core.tests.fixtures import UserFactory
from core.models import User
from apps.manager.tests.fixtures import ManagerFactory
from ..models import Section, Topic, Comment
from .fixtures import SectionFactory, TopicFactory, CommentFactory, NotificationFactory


class SectionTestCase(LoginWithUserTestCase):

    def test_list_smoke(self):
        response = self.client.get(reverse('forum:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/section_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('forum:section-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/section_add.html')

    def test_ok_create_initial(self):
        response = self.client.get(reverse('forum:section-add'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['author'].value(), self.user.pk)

    def test_ok_create(self):
        response = self.client.post(
            reverse('forum:section-add'),
            {'author': self.user.pk, 'title': 'section title', 'description': 'section description'})
        self.assertRedirects(response, reverse('forum:list'))
        self.assertEqual(Section.objects.count(), 1)

    def test_update_smoke(self):
        section = SectionFactory()
        response = self.client.get(reverse('forum:section-update', args=(section.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/section_update.html')

    def test_ok_update(self):
        section = SectionFactory()
        data = {
            'author': section.author.pk,
            'title': 'updated title',
            'description': 'updated description'
        }
        response = self.client.post(reverse('forum:section-update', args=(section.pk,)), data)

        self.assertRedirects(response, reverse('forum:list'))
        self.assertDictEqual(Section.objects.filter(pk=section.pk).values(*data.keys())[0], data)


class TopicTestCase(LoginWithUserTestCase):

    def setUp(self):
        super(TopicTestCase, self).setUp()
        self.forum_section = SectionFactory()

    def test_list_smoke(self):
        response = self.client.get(reverse('forum:topic-list', args=(self.forum_section.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('forum:topic-add'), {'section': self.forum_section.pk})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_add.html')

    def test_ok_create_initial(self):
        response = self.client.get(reverse('forum:topic-add'), {'section': self.forum_section.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['author'].value(), self.user.pk)
        self.assertEqual(response.context['form']['section'].value(), self.forum_section.pk)

    def test_ok_create(self):
        response = self.client.post(
            reverse('forum:topic-add'),
            {'author': self.user.pk, 'section': self.forum_section.pk, 'title': 'topic title', 'text': 'topic text'},
            QUERY_STRING=urlencode({'section': self.forum_section.pk}))

        self.assertRedirects(response, reverse('forum:topic-list', args=(self.forum_section.pk,)))
        self.assertEqual(Topic.objects.count(), 1)

    def test_update_smoke(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-update', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_update.html')

    def test_ok_update(self):
        topic = TopicFactory(section=self.forum_section)
        data = {
            'author': topic.author.pk,
            'section': self.forum_section.pk,
            'title': 'updated title',
            'text': 'updated text'
        }
        response = self.client.post(reverse('forum:topic-update', args=(topic.pk,)), data)

        self.assertRedirects(response, reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertDictEqual(Topic.objects.filter(pk=topic.pk).values(*data.keys())[0], data)

    def test_detail_smoke(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_detail.html')

    def test_ok_detail_initial(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['topic'].value(), topic.pk)
        self.assertEqual(response.context['form']['author'].value(), self.user.pk)

    def test_ok_create_comment(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.post(
            reverse('forum:topic-detail', args=(topic.pk,)),
            {'author': self.user.pk, 'topic': topic.pk, 'text': 'topic text'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)

    def test_notify_smoke(self):
        response = self.client.get(reverse('forum:topic-notify'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_notify.html')

    def test_ok_notify_list(self):
        topic = TopicFactory(section=self.forum_section)
        NotificationFactory(topic=topic, user=self.user)
        other_topic = TopicFactory()
        NotificationFactory(topic=other_topic, user=self.user)
        other_topic = TopicFactory()
        other_user = UserFactory()
        NotificationFactory(topic=other_topic, user=other_user)

        response = self.client.get(reverse('forum:topic-notify'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 2)

    def test_delete_smoke(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-delete', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_delete.html')

    def test_ok_delete(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.post(reverse('forum:topic-delete', args=(topic.pk,)))
        self.assertRedirects(response, reverse('forum:topic-list', args=(self.forum_section.pk,)))
        self.assertEqual(Topic.objects.count(), 0)

    def test_close_smoke(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-close', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_close.html')

    def test_ok_close_author(self):
        topic = TopicFactory(author=self.user, section=self.forum_section)
        response = self.client.post(reverse('forum:topic-close', args=(topic.pk,)))
        self.assertRedirects(response, reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertTrue(Topic.objects.get(pk=topic.pk).closed)

    def test_ok_close_administrator(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.post(reverse('forum:topic-close', args=(topic.pk,)))
        self.assertRedirects(response, reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertTrue(Topic.objects.get(pk=topic.pk).closed)

    def test_fail_close(self):
        self.user.type = User.UserType.manager
        self.user.save()
        ManagerFactory(user=self.user)
        topic = TopicFactory(section=self.forum_section)
        response = self.client.post(reverse('forum:topic-close', args=(topic.pk,)))
        self.assertRedirects(response, reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertFalse(Topic.objects.get(pk=topic.pk).closed)


class CommentTestCase(LoginWithUserTestCase):

    def test_update_smoke(self):
        comment = CommentFactory()
        response = self.client.get(reverse('forum:comment-update', args=(comment.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/comment_update.html')

    def test_ok_update(self):
        comment = CommentFactory()
        data = {
            'author': comment.author.pk,
            'topic': comment.topic.pk,
            'text': 'updated text'
        }
        response = self.client.post(
            reverse('forum:comment-update', args=(comment.pk,)), data)
        self.assertRedirects(response, reverse('forum:topic-detail', args=(comment.topic.pk,)))
        self.assertDictEqual(Comment.objects.filter(pk=comment.pk).values(*data.keys())[0], data)

    def test_delete_smoke(self):
        comment = CommentFactory()
        response = self.client.get(reverse('forum:comment-delete', args=(comment.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/comment_delete.html')

    def test_delete_ok(self):
        comment = CommentFactory()
        response = self.client.post(reverse('forum:comment-delete', args=(comment.pk,)))
        self.assertRedirects(response, comment.topic.get_absolute_url())
        self.assertEqual(Comment.objects.count(), 0)
