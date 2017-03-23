# coding=utf-8
from django.core.urlresolvers import reverse

from core.models import User
from core.tests.base import LoginWithUserTestCase


class AgencyTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('agency:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('agency/agency_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('agency:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('agency/agency_add.html')

    def test_create(self):
        response = self.client.post(
            reverse('agency:add'),
            {'email': 'some_agency@agency.ag', 'password1': 'password', 'password2': 'password'})
        some_agency = User.objects.get(email='some_agency@agency.ag')
        self.assertRedirects(response, reverse('agency:update', args=(some_agency.pk,)))
        self.assertEqual(some_agency.type, User.UserType.agency)
        self.assertEqual(some_agency.is_staff, True)
        self.assertEqual(some_agency.is_active, True)

    def test_create_leader(self):
        response = self.client.post(
            reverse('agency:add'),
            {'email': 'some_leader_agency@agency.ag', 'password1': 'password', 'password2': 'password', 'leader': ''})
        some_agency = User.objects.get(email='some_leader_agency@agency.ag')
        self.assertRedirects(response, reverse('agency:update', args=(some_agency.pk,)))
        self.assertEqual(some_agency.type, User.UserType.agency)
        self.assertEqual(some_agency.is_staff, True)
        self.assertEqual(some_agency.is_active, True)
        self.assertEqual(some_agency.agency_leader, True)

    def create_some_agency(self):
        return User.objects.create_user(
            email='some_agency@agency',
            password='123456',
            last_name='some',
            first_name='agency',
            patronymic='ag',
            phone='+70000000000'
        )

    def test_update_smoke(self):
        some_agency = self.create_some_agency()
        response = self.client.get(reverse('agency:update', args=(some_agency.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('agency/agency_update.html')

    def test_update(self):
        some_agency = self.create_some_agency()
        response = self.client.get(reverse('agency:update', args=(some_agency.pk,)))
        response = self.client.post(
            reverse('administrator:update', args=(some_agency.pk,)), response.context['form'].initial)
        self.assertEqual(response.status_code, 200)
