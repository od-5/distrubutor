# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import ManagerFactory


class ManagerTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('manager:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/manager_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('manager:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/manager_add.html')

    def test_update_smoke(self):
        manager = ManagerFactory()
        response = self.client.get(reverse('manager:update', args=(manager.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/manager_update.html')

    def test_report_smoke(self):
        response = self.client.get(reverse('manager:report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/manager_report.html')
