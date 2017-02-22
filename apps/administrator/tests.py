# coding=utf-8
from django.core.urlresolvers import reverse

from core.models import User
from .base_test import LoginWithAdminTestCase


class AdministratorTestCase(LoginWithAdminTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('administrator:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrator/administrator_list.html')

    def test_list_filter(self):
        response = self.client.get(
            reverse('administrator:list'),
            {
                'email': self.admin_user.email,
                'last_name': self.admin_user.last_name,
                'first_name': self.admin_user.first_name,
                'patronymic': self.admin_user.patronymic,
                'phone': self.admin_user.phone
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)
        self.assertEqual(response.context['object_list'][0], self.admin_user)

    def test_create_smoke(self):
        response = self.client.get(reverse('administrator:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrator/administrator_add.html')

    def test_create(self):
        response = self.client.post(
            reverse('administrator:add'),
            {'email': 'some_admin@admin.ad', 'password1': 'password', 'password2': 'password'})
        some_admin = User.objects.get(email='some_admin@admin.ad')
        self.assertRedirects(response, reverse('administrator:update', args=(some_admin.pk,)))
        self.assertEqual(some_admin.type, 1)
        self.assertEqual(some_admin.is_superuser, True)
        self.assertEqual(some_admin.is_staff, True)
        self.assertEqual(some_admin.is_active, True)

    def test_update_smoke(self):
        response = self.client.get(reverse('administrator:update', args=(self.admin_user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrator/administrator_update.html')

    def test_update(self):
        response = self.client.get(reverse('administrator:update', args=(self.admin_user.pk,)))
        response = self.client.post(
            reverse('administrator:update', args=(self.admin_user.pk,)), response.context['form'].initial)
        self.assertEqual(response.status_code, 200)
