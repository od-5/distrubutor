# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from core.models import User
from apps.geolocation.models import City
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from .models import Client


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
        city = City(name=u'Город')
        city.save()

        moderator = Moderator(company=u'Компания', user=self.user)
        moderator.save()

        manager_user = User.objects.create_user('manager@manager.ma', '123456', type=5)
        manager = Manager(user=manager_user, moderator=self.user)
        manager.save()

        client = Client(name=u'Клиент', moderator=moderator, manager=manager, city=city)
        client.save()

        response = self.client.get(reverse('client:update', args=(client.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_update.html')
