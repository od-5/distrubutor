# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from apps.geolocation.models import City
from apps.manager.models import Manager
from .fixtures import ClientFactory, ClientContactFactory, TaskFactory


class ClientTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('client:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_list.html')

    def test_list_filter(self):
        client = ClientFactory()
        ClientContactFactory(client=client)
        response = self.client.get(
            reverse('client:list'),
            {
                'name': client.name,
                'phone': client.clientcontact_set.all()[0].phone,
                'contact': client.clientcontact_set.all()[0].name,
                'manager': client.manager.pk,
                'city': client.city.pk
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)
        self.assertEqual(response.context['object_list'][0], client)

    def test_list_context(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:list'), {'client_name': client.name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['manager_client_count'], 1)
        self.assertEqual(response.context['manager_task_count'], 0)
        self.assertEqual(
            response.context['manager_list'].count(), Manager.objects.filter(user__is_active=True).count())
        self.assertEqual(response.context['city_list'].count(), City.objects.all().count())
        self.assertIn('import_form', response.context)
        # TODO: для полноты нужна проверка для других типов пользователей

    def test_list_search_client_name(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:list'), {'client_name': client.name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_client_list'].count(), 1)
        self.assertEqual(response.context['search_client_list'][0], client)

    def test_create_smoke(self):
        response = self.client.get(reverse('client:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_add.html')

    def test_update_smoke(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:update', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_update.html')


class ClientManagerHistoryTestCase(LoginWithUserTestCase):
    def test_smoke(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:history', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientmanager_history.html')


class ClientContactTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:contact-list', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientcontact_list.html')

    def test_create_smoke(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:contact-add', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientcontact_add.html')

    def test_update_smoke(self):
        client = ClientFactory()
        client_contact = ClientContactFactory(client=client)
        response = self.client.get(reverse('client:contact-update', args=(client_contact.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientcontact_update.html')


class ClientTaskTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('client:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('client:task-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_add.html')

    def test_update_smoke(self):
        task = TaskFactory()
        response = self.client.get(reverse('client:task-update', args=(task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_update.html')
