# coding=utf-8
from django.test import TestCase

from core.tests.fixtures import UserFactory
from ..models import Client, Task
from .fixtures import ClientFactory, TaskFactory


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


class TaskModelTestCase(TestCase):
    def test_get_qs(self):
        task = TaskFactory()

        administrator_user = UserFactory()
        self.assertEqual(Task.objects.get_qs(administrator_user).count(), Task.objects.all().count())

        moderator_user = task.client.moderator.user
        task_qs = Task.objects.get_qs(moderator_user)
        for tsk in task_qs:
            self.assertEqual(tsk.manager.moderator, moderator_user)

        manager_user = task.client.manager.user
        task_qs = Task.objects.get_qs(manager_user)
        for tsk in task_qs:
            self.assertEqual(tsk.manager, task.manager)

        manager_user.leader = True
        manager_user.save()
        task_qs = Task.objects.get_qs(manager_user)
        for tsk in task_qs:
            self.assertEqual(tsk.manager.moderator, task.manager.moderator)
