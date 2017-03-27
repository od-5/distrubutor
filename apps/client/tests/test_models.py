# coding=utf-8
from django.test import TestCase

from core.tests.fixtures import UserFactory
from ..models import Client
from .fixtures import ClientFactory


class ClientModelTestCase(TestCase):
    def test_get_qs(self):
        client = ClientFactory()

        administrator_user = UserFactory()
        self.assertEqual(Client.objects.get_qs(administrator_user).count(), Client.objects.all().count())

        moderator_user = client.moderator.user
        client_qs = Client.objects.get_qs(moderator_user)
        for clnt in client_qs:
            self.assertEqual(clnt.moderator, client.moderator)

        manager_user = client.manager.user
        client_qs = Client.objects.get_qs(manager_user)
        for clnt in client_qs:
            self.assertEqual(clnt.manager, client.manager)
