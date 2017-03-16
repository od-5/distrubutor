# coding=utf-8
from datetime import datetime

from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from core.models import User
from apps.geolocation.models import City
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from .models import Client, ClientContact, Task


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

    # Тест формирования queryset
    #   проверка фильтрации в зависимости от типа пользователя
    #   проверка фильтрации по полям
    # Тест формирования context

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
