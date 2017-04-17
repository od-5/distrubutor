# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import SectionFactory, TopicFactory, CommentFactory


class SectionTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('forum:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/section_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('forum:section-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/section_add.html')

    def test_update_smoke(self):
        section = SectionFactory()
        response = self.client.get(reverse('forum:section-update', args=(section.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/section_update.html')


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

    def test_update_smoke(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-update', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_update.html')

    def test_detail_smoke(self):
        topic = TopicFactory(section=self.forum_section)
        response = self.client.get(reverse('forum:topic-detail', args=(topic.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_detail.html')

    def test_notify_smoke(self):
        response = self.client.get(reverse('forum:topic-notify'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic_notify.html')


class CommentTestCase(LoginWithUserTestCase):
    def test_update_smoke(self):
        comment = CommentFactory()
        response = self.client.get(reverse('forum:comment-update', args=(comment.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/comment_update.html')
