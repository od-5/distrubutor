# coding=utf-8
from datetime import datetime

from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from core.models import User
from apps.moderator.models import Moderator
from apps.sale.models import Sale, SaleOrder
from apps.geolocation.models import City
from .models import Distributor, DistributorTask


def _create_fake_distributor():
    moderator_user = User.objects.create_user('moderator@moderator.mo', '123456', type=2)
    moderator = Moderator(user=moderator_user)
    moderator.save()

    distributor_user = User.objects.create_user('distributor@distributor.di', '123456', type=4)
    distributor = Distributor(user=distributor_user, moderator=moderator)
    distributor.save()

    return distributor


def _create_fake_distributor_task():
        distributor = _create_fake_distributor()

        city = City(name=u'Город')
        city.save()

        sale_user = User.objects.create_user('sale@sale.sa', '123456', type=3)
        sale = Sale(user=sale_user, moderator=distributor.moderator, city=city, legal_name=u'Клиент')
        sale.save()

        order = SaleOrder(sale=sale, date_start=datetime.now())
        order.save()

        distributor_task = DistributorTask(distributor=distributor, sale=sale, order=order, date=datetime.now())
        distributor_task.save()

        return distributor_task


class DistributorTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('distributor:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/distributor_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('distributor:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/distributor_add.html')

    def test_update_smoke(self):
        distributor = _create_fake_distributor()
        response = self.client.get(reverse('distributor:update', args=(distributor.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/distributor_update.html')


class DistributorTaskTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('distributor:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_list.html')

    def test_archive_smoke(self):
        response = self.client.get(reverse('distributor:task-archive'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('distributor:task-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_add.html')

    def test_update_smoke(self):
        distributor_task = _create_fake_distributor_task()
        response = self.client.get(reverse('distributor:task-update', args=(distributor_task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_update.html')

    def test_update_map_smoke(self):
        distributor_task = _create_fake_distributor_task()
        response = self.client.get(reverse('distributor:task-update-map', args=(distributor_task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_update_map.html')


class DstributorPromoTaskTestCase(LoginWithUserTestCase):
    pass


class DistributorQuestTaskTestCase(LoginWithUserTestCase):
    pass
