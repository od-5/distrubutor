# coding=utf-8
from core.tests.base import LoginWithUserTestCase
from ..forms import SectionForm, TopicForm, CommentForm
from ..models import Section, Topic, Comment
from .fixtures import SectionFactory, TopicFactory


class SectionTestCase(LoginWithUserTestCase):

    def test_ok_init(self):
        self.assertTrue(SectionForm())

    def test_ok_valid(self):
        data = {
            'author': self.user.pk,
            'title': 'section title',
            'description': 'section description'
        }
        form = SectionForm(data)

        self.assertTrue(form.is_valid())
        section = form.save()
        self.assertDictEqual(Section.objects.filter(pk=section.pk).values(*data.keys())[0], data)

    def test_fail_invalid(self):
        form = SectionForm({})
        self.assertFalse(form.is_valid())


def TopicTestCase(LoginWithUserTestCase):

    def test_ok_init(self):
        self.assertTrue(TopicForm())

    def test_ok_valid(self):
        data = {
            'author': self.user.pk,
            'section': SectionFactory(),
            'title': 'topic title',
            'text': 'topic text'
        }
        form = TopicForm(data)

        self.assertTrue(form.is_valid())
        topic = form.save()
        self.assertDictEqual(Topic.objects.filter(pk=topic.pk).values(*data.keys())[0], data)

    def test_fail_invalid(self):
        form = TopicForm({})
        self.assertFalse(form.is_valid())


def CommentTestCase(LoginWithUserTestCase):

    def test_ok_init(self):
        self.assertTrue(CommentForm())

    def test_ok_valid(self):
        data = {
            'author': self.user.pk,
            'topic': TopicFactory(),
            'text': 'topic text'
        }
        form = CommentForm(data)

        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertDictEqual(Comment.objects.filter(pk=comment.pk).values(*data.keys())[0], data)

    def test_fail_invalid(self):
        form = CommentForm()
        self.assertFalse(form.is_valid())
