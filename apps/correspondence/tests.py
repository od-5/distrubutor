# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .models import Message, UserMessage


class MessageTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('correspondence:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correspondence/message_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('correspondence:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correspondence/message_add.html')

    def test_detail_smoke(self):
        message = Message(title=u'Тема', text=u'Текст', author=self.user)
        message.save()

        response = self.client.get(reverse('correspondence:detail', args=(message.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correspondence/message_detail.html')


class UserMessageTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('correspondence:usermessage-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correspondence/usermessage_list.html')

    def test_detail_smoke(self):
        message = Message(title=u'Тема', text=u'Текст', author=self.user)
        message.save()
        user_message = UserMessage(message=message, recipient=self.user)
        user_message.save()

        response = self.client.get(reverse('correspondence:usermessage-detail', args=(user_message.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'correspondence/usermessage_detail.html')

    def test_answer_add_smoke(self):
        response = self.client.get(reverse('correspondence:usermessage-answer-add'))
        self.assertRedirects(response, reverse('correspondence:usermessage-list'))
