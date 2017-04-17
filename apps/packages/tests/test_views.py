# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import PackageFactory


class PackageTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('package:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/package_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('package:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/package_add.html')

    def test_update_smoke(self):
        package = PackageFactory()
        response = self.client.get(reverse('package:update', args=(package.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'packages/package_update.html')
