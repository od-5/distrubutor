# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase


class DashboardTestCase(LoginWithUserTestCase):
    def test_smoke(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dash_admin.html')
