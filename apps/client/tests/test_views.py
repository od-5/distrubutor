# coding=utf-8
from datetime import date

from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from apps.geolocation.models import City
from apps.geolocation.tests.fixtures import CityFactory
from apps.manager.models import Manager
from apps.manager.tests.fixtures import ManagerFactory
from apps.moderator.tests.fixtures import ModeratorFactory
from ..models import Task
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

    def test_create(self):
        city = CityFactory()
        moderator = ModeratorFactory()
        manager = ManagerFactory(moderator=moderator.user)

        response = self.client.post(
            reverse('client:add'),
            {
                'moderator': moderator,
                'manager': manager,
                'name': u'Клиент',
                'city': city
            })
        self.assertEqual(response.status_code, 200)

    def test_update_smoke(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:update', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_update.html')

    def test_update(self):
        client = ClientFactory()
        response = self.client.get(reverse('client:update', args=(client.pk,)))
        response = self.client.post(reverse('client:update', args=(client.pk,)), response.context['form'].initial)
        self.assertEqual(response.status_code, 200)


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

    def test_create(self):
        client = ClientFactory()
        response = self.client.post(
            reverse('client:contact-add', args=(client.pk,)),
            {'client': client.pk, 'name': u'Контактное лицо'})
        self.assertRedirects(response, reverse('client:contact-list', args=(client.pk,)))

    def test_update_smoke(self):
        client = ClientFactory()
        client_contact = ClientContactFactory(client=client)

        response = self.client.get(reverse('client:contact-update', args=(client_contact.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientcontact_update.html')

    def test_update(self):
        client = ClientFactory()
        client_contact = ClientContactFactory(client=client)

        response = self.client.get(reverse('client:contact-update', args=(client_contact.pk,)))
        response = self.client.post(
            reverse('client:contact-update', args=(client_contact.pk,)),
            response.context['form'].initial)
        self.assertRedirects(response, reverse('client:contact-list', args=(client.pk,)))


class ClientTaskTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('client:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_list.html')

    # TODO: протестировать после причесывания вида
    # def test_list(self):
    #     pass

    def test_create_smoke(self):
        response = self.client.get(reverse('client:task-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_add.html')

    def test_create(self):
        client = ClientFactory()
        response = self.client.post(
            reverse('client:task-add'),
            {
                'manager': client.manager.pk,
                'client': client.pk,
                'type': Task.TaskType.planned_meet,
                'status': Task.TaskStatus.planned,
                'date': date.today()
            })
        created_task = Task.objects.get(client=client)
        self.assertRedirects(response, reverse('client:task-update', args=(created_task.pk,)))

    def test_update_smoke(self):
        task = TaskFactory()
        response = self.client.get(reverse('client:task-update', args=(task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_update.html')

    def test_update(self):
        task = TaskFactory()
        response = self.client.get(reverse('client:task-update', args=(task.pk,)))
        response = self.client.post(reverse('client:task-update', args=(task.pk,)), response.context['form'].initial)
        self.assertEqual(response.status_code, 200)
