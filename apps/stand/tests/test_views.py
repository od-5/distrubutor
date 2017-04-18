# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import StandFactory


class StandTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('stand:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stand/stand_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('stand:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stand/stand_add.html')

    def test_update_smoke(self):
        stand = StandFactory()
        response = self.client.get(reverse('stand:update', args=(stand.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stand/stand_form.html')
