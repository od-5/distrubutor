# coding=utf-8
from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from core.models import User
from apps.geolocation.models import City
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from .models import Client, ClientContact, Task


class ClientModelTestCase(TestCase):
    def test_get_qs(self):
        city = City(name=u'Город')
        city.save()

        moderator_user = User.objects.create_user('moderator@moderator.mo', '123456', type=2)

        moderator = Moderator(company=u'Компания', user=moderator_user)
        moderator.save()

        manager_user = User.objects.create_user('manager@manager.ma', '123456', type=5)
        manager = Manager(user=manager_user, moderator=moderator_user)
        manager.save()

        Client(name=u'Клиент1', moderator=moderator, manager=manager, city=city).save()

        user = User.objects.create_user('user@user.us', '123456', type=1)

        self.assertEqual(Client.objects.get_qs(user).count(), Client.objects.all().count())

        client_qs = Client.objects.get_qs(moderator_user)
        for client in client_qs:
            self.assertEqual(client.moderator, moderator)

        client_qs = Client.objects.get_qs(manager_user)
        for client in client_qs:
            self.assertEqual(client.manager, manager)


def _create_fake_client():
    city = City(name=u'Город')
    city.save()

    moderator_user = User.objects.create_user('moderator@moderator.mo', '123456', type=2)

    moderator = Moderator(company=u'Компания', user=moderator_user)
    moderator.save()

    manager_user = User.objects.create_user('manager@manager.ma', '123456', type=5)
    manager = Manager(user=manager_user, moderator=moderator_user)
    manager.save()

    client = Client(name=u'Клиент', moderator=moderator, manager=manager, city=city)
    client.save()

    return client


class ClientTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('client:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_list.html')

    def test_list_filter(self):
        client = _create_fake_client()
        ClientContact(client=client, name=u'Контактное лицо', phone=u'1111111111').save()

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
        client = _create_fake_client()

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
        client = _create_fake_client()

        response = self.client.get(reverse('client:list'), {'client_name': client.name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_client_list'].count(), 1)
        self.assertEqual(response.context['search_client_list'][0], client)

    def test_create_smoke(self):
        response = self.client.get(reverse('client:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_add.html')

    def test_update_smoke(self):
        client = _create_fake_client()
        response = self.client.get(reverse('client:update', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_update.html')


class ClientManagerHistoryTestCase(LoginWithUserTestCase):
    def test_smoke(self):
        client = _create_fake_client()
        response = self.client.get(reverse('client:history', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientmanager_history.html')


class ClientContactTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        client = _create_fake_client()
        response = self.client.get(reverse('client:contact-list', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientcontact_list.html')

    def test_create_smoke(self):
        client = _create_fake_client()
        response = self.client.get(reverse('client:contact-add', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/clientcontact_add.html')

    def test_update_smoke(self):
        client = _create_fake_client()
        client_contact = ClientContact(client=client, name=u'Контактное лицо')
        client_contact.save()
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
        client = _create_fake_client()
        client_contact = ClientContact(client=client, name=u'Контактное лицо')
        client_contact.save()
        task = Task(
            manager=client.manager,
            client=client,
            clientcontact=client_contact,
            type=0,
            date=datetime.now()
        )
        task.save()
        response = self.client.get(reverse('client:task-update', args=(task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/task_update.html')