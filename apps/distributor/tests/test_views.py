# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from ..models import DistributorTask
from .fixtures import DistributorFactory, DistributorTaskFactory


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
        distributor = DistributorFactory()
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
        distributor_task = DistributorTaskFactory()
        response = self.client.get(reverse('distributor:task-update', args=(distributor_task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_update.html')

    def test_update_map_smoke(self):
        distributor_task = DistributorTaskFactory()
        response = self.client.get(reverse('distributor:task-update-map', args=(distributor_task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'distributor/task_update_map.html')


class DstributorPromoTaskTestCase(LoginWithUserTestCase):
    def test_create_smoke(self):
        response = self.client.get(reverse('distributor:task-promo-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('distributor/task_promo_add.html')

    def test_update_smoke(self):
        distributor_task = DistributorTaskFactory(category=DistributorTask.TaskCategory.promo_action)
        response = self.client.get(reverse('distributor:task-promo-update', args=(distributor_task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('distributor/task_promo_update.html')


class DistributorQuestTaskTestCase(LoginWithUserTestCase):
    def test_create_smoke(self):
        response = self.client.get(reverse('distributor:task-quest-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('distributor/task_quest_add.html')

    def test_update_smoke(self):
        distributor_task = DistributorTaskFactory(category=DistributorTask.TaskCategory.questioning)
        response = self.client.get(reverse('distributor:task-quest-update', args=(distributor_task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('distributor/task_quest_update.html')


class GPSPointTestCase(LoginWithUserTestCase):
    # TODO:
    pass


class DistributorReportTestCase(LoginWithUserTestCase):
    def test_report_smoke(self):
        response = self.client.get(reverse('distributor:report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('distributor/distributor_report.html')
